# Goal-based agent

function GOAL-BASED-AGENT(percept) returns action:
    persistent: 
    state, what the current agent sees as the world state
    model, a description detailing how the next state is a result of the current state and StopAsyncIteration
    state, what the current agent sees as the world state
    goals, a set of goals the agent needs to accomplish (similar to a reflex agent's rules)
    action, the action that most recently occurred and is initially null
    state UPDATE-STATE(state, action, percept, model)
    action BEST-ACTION(goals, state)
    return action

function BEST-ACTION:
    determines the action that most furthers the agent towards fulfilling its gloals


# Utility-based pseudocode

function UTILITY-BASED-AGENT (percept) returns action:
    persistent:
    state, what the current agent sees as the world state
    goals, a set of goals the agent needs to accomplish (similar to a reflex agent's rules)
    utility, internal performance measurement
    action, the action that most recently occurred and is initially null
    state UPDATE-STATE(state, action, percept, model)
    utility UTILITY-FUNCTION(goals, state)
    action BEST-ACTION(goals, state, utility)
    return action

UTILITY-function calculates the utility of the possible actions given the state and goals.
BEST-ACTION is updated from above to take the utility of each action into account when choosing the best action.