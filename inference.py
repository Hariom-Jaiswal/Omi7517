import os
import json
from openai import OpenAI
from env.environment import OpsDeskEnv
from env.models import Action

def run_inference():
    api_key = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY", "dummy_token")
    base_url = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
    model_name = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
    
    task_name = "opsdesk-hard"
    benchmark = "OpsDesk"

    client = OpenAI(api_key=api_key, base_url=base_url)
    
    env = OpsDeskEnv(task_level="HARD", max_steps=5)
    obs = env.reset()
    
    print(f"[START] task={task_name} env={benchmark} model={model_name}", flush=True)
    
    terminated = False
    step_num = 1
    rewards = []
    history = []
    
    while not terminated:
        history_block = "\n".join(history[-4:]) if history else "None"
        prompt = f"""You are an AI operations assistant handling emails.
Step: {step_num}
Previous actions:
{history_block}

Current Observation: {obs.model_dump_json(indent=2)}

Available Actions: classify_email, extract_task, schedule_meeting, reply_email, ignore_email.
Return JSON ONLY in this format: {{"action_type": "...", "email_id": "...", "metadata": {{"classification": "urgent", "meeting_time": "2 PM"}}}}"""
        
        try:
            resp = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            content = resp.choices[0].message.content or "{}"
            # Clean possible markdown wrap to ensure valid JSON parsing
            content = content.replace("```json", "").replace("```", "").strip()
            action_data = json.loads(content)
            action = Action(**action_data)
            error_val = "null"
        except Exception as e:
            action = Action(action_type="ignore_email", email_id="e1")
            error_val = str(e).replace('\n', ' ')
            
        obs, reward, terminated, info = env.step(action)
        rewards.append(reward.value)
        action_str = f"{action.action_type}({action.email_id})"
        done_val = str(terminated).lower()
        
        history.append(f"Step {step_num}: Action={action_str}, Reward={reward.value:.2f}")
        
        print(f"[STEP] step={step_num} action={action_str} reward={reward.value:.2f} done={done_val} error={error_val}", flush=True)
        step_num += 1
        
    score = info.get("score", 0.0)
    score_clamped = min(max(score, 0.0), 1.0)
    success = score_clamped >= 0.5
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    
    print(f"[END] success={str(success).lower()} steps={step_num-1} score={score_clamped:.3f} rewards={rewards_str}", flush=True)

if __name__ == "__main__":
    run_inference()
