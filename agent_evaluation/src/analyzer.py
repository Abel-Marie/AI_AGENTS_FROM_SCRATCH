def analyze_results(results=None):
    """Analyzes evaluation results and provides insights.
    
    Args:
        results: Optional evaluation results. If None, shows example analysis.
    """
    print("📊 Understanding Evaluation Results:")
    print()
    print("🔍 EXAMPLE ANALYSIS:")
    print()
    print("Test Case: living_room_light_on")
    print("  ❌ response_match_score: 0.45/0.80")
    print("  ✅ tool_trajectory_avg_score: 1.0/1.0")
    print()
    print("📈 What this tells us:")
    print("• TOOL USAGE: Perfect - Agent used correct tool with correct parameters")
    print("• RESPONSE QUALITY: Poor - Response text too different from expected")
    print("• ROOT CAUSE: Agent's communication style, not functionality")
    print()
    print("🎯 ACTIONABLE INSIGHTS:")
    print("1. Technical capability works (tool usage perfect)")
    print("2. Communication needs improvement (response quality failed)")
    print("3. Fix: Update agent instructions for clearer language or constrained response.")
    print()

def print_detailed_analysis():
    """Prints detailed analysis of common evaluation patterns."""
    print("\n" + "="*60)
    print("📊 EVALUATION METRICS EXPLAINED")
    print("="*60)
    
    print("\n🎯 tool_trajectory_avg_score (1.0 = Perfect)")
    print("   Measures: Did the agent use the RIGHT tools with RIGHT parameters?")
    print("   Pass: Agent calls set_device_status('living room', 'floor lamp', 'ON')")
    print("   Fail: Agent calls set_device_status('bedroom', 'floor lamp', 'ON')")
    print("   Fail: Agent doesn't call any tool")
    
    print("\n📝 response_match_score (0.8 = 80% similarity)")
    print("   Measures: How similar is the response to the expected text?")
    print("   Pass: 'Successfully set the floor lamp in the living room to on.'")
    print("   Fail: 'I have turned on your lamp! It should be bright now!'")
    print("   Why: Different wording, extra information, or wrong format")
    
    print("\n💡 COMMON FAILURE PATTERNS:")
    print("   1. Hallucination: Agent claims capabilities it doesn't have")
    print("   2. Wrong Parameters: Correct tool, wrong location/device/status")
    print("   3. Verbose Responses: Too much extra text reduces match score")
    print("   4. No Tool Use: Agent responds without calling required tools")
    
    print("\n🔧 HOW TO FIX FAILURES:")
    print("   • Tool failures → Update agent instructions or tool descriptions")
    print("   • Response failures → Constrain response format in instructions")
    print("   • Hallucinations → Add explicit capability boundaries")
    print("="*60 + "\n")

def compare_expected_vs_actual(test_case_id, expected, actual):
    """Compares expected vs actual results for a test case."""
    print(f"\n🔍 Test Case: {test_case_id}")
    print("-" * 50)
    print("Expected Response:")
    print(f"  {expected}")
    print("\nActual Response:")
    print(f"  {actual}")
    print("-" * 50)
