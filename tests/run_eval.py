import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from google.adk.evaluation import AgentEvaluator

load_dotenv()

async def main():
    print("🚀 Starting Agent Evaluation...")
    
    # We evaluate idea_intake_agent
    agent_module = "tests.evaluation.test_agent"
    
    # Test file path
    test_file = str(project_root / "tests/evaluation/test_idea_intake.test.json")
    
    try:
        await AgentEvaluator.evaluate(
            agent_module=agent_module,
            eval_dataset_file_path_or_dir=test_file,
            num_runs=1,
            print_detailed_results=True
        )
        print("✅ Evaluation completed.")
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
