from google.genai import types
from google.adk.runners import Runner

async def run_session(
    runner_instance: Runner, user_queries: list[str] | str = None, session_id: str = "default", app_name: str = "MemoryDemoApp", user_id: str = "demo_user", interactive: bool = False
):
    """Helper function to run queries in a session and display responses."""
    print(f"\n### Session: {session_id}")

    session_service = runner_instance.session_service

    # Create or retrieve session
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
    except:
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

    # Process queries
    if interactive:
        print("Type 'exit' or 'quit' to end the session.")
        while True:
            query = input(f"\nUser > ").strip()
            if query.lower() in ["exit", "quit"]:
                break
            
            if not query:
                continue

            # Convert the query string to the ADK Content format
            query_content = types.Content(role="user", parts=[types.Part(text=query)])

            # Stream the agent's response asynchronously
            async for event in runner_instance.run_async(
                user_id=user_id, session_id=session.id, new_message=query_content
            ):
                # Check if the event contains valid content
                if event.content and event.content.parts:
                    # Filter out empty or "None" responses before printing
                    for part in event.content.parts:
                        if part.text and part.text != "None":
                            print(f"Agent > ", part.text)

    elif user_queries:
        # Convert single query to list
        if isinstance(user_queries, str):
            user_queries = [user_queries]

        # Process each query
        for query in user_queries:
            print(f"\nUser > {query}")
            query_content = types.Content(role="user", parts=[types.Part(text=query)])

            # Stream agent response
            async for event in runner_instance.run_async(
                user_id=user_id, session_id=session.id, new_message=query_content
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    text = event.content.parts[0].text
                    if text and text != "None":
                        print(f"Model: > {text}")
    else:
        print("No queries!")
