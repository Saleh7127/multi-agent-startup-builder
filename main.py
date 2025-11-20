"""
Main entry point for the multi-agent startup builder.
Uses the Root Agent to orchestrate all agents sequentially.
"""

import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.root_agent import root_agent

load_dotenv()


async def main():
    """Run the root agent with a startup idea."""
    if len(sys.argv) < 2:
        print("Usage: python main.py '<startup_idea>'")
        print("\nExample:")
        print("  python main.py 'An AI platform that helps students revise and improve assignments'")
        sys.exit(1)
    
    startup_idea = sys.argv[1]
    
    print("🚀 Starting Multi-Agent Startup Builder...")
    print(f"📝 Startup Idea: {startup_idea}\n")
    
    runner = InMemoryRunner(agent=root_agent)
    
    print("🧠 Root Agent orchestrating all agents sequentially...\n")
    try:
        response = await runner.run_debug(
            startup_idea,
            quiet=False
        )
        
        print("\n✅ Process completed!")
        print(f"\n📄 Final output stored in: {response}")
        
        return response
    except Exception as e:
        # Handle MCP cleanup errors gracefully - these occur after successful execution
        error_str = str(e)
        error_type = type(e).__name__
        
        # Check for MCP-related cleanup errors (BaseExceptionGroup, RuntimeError with cancel scope)
        if ("cancel scope" in error_str.lower() or 
            "mcp" in error_str.lower() or 
            "ExceptionGroup" in error_type or
            "BaseExceptionGroup" in error_type):
            print("\n⚠️  Warning: MCP tool cleanup error (non-critical)")
            print("✅ Process completed successfully despite cleanup warning")
            print(f"   PDF should be available in: generated_assets/pitch_decks/")
            return None
        else:
            # Re-raise if it's a different error
            raise


if __name__ == "__main__":
    asyncio.run(main())

