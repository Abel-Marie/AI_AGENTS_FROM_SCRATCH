from google.adk.runners import InMemoryRunner

async def run_agent_debug(agent, query):
    """Runs the agent in debug mode and prints the output."""
    print(f"🚀 Running agent: {agent.name}")
    runner = InMemoryRunner(agent=agent)
    
    try:
        response = await runner.run_debug(query)
        # Check if response is iterable (async generator) or a single object
        if hasattr(response, '__aiter__'):
             async for event in response:
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(f"Agent > {part.text}")
        else:
            # Handle non-streaming response if applicable
             print(f"Response: {response}")

    except Exception as e:
        print(f"❌ Error running agent: {e}")
        print("💡 Check 'logger.log' for detailed error trace.")
