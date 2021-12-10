# This is a coding sample from my CS136 Final Project: Reinforcement Learning in Matching Mechanisms, Fall 2021.
# I create a function to run the Student-Proposing Deferred Acceptance Algorithm that will be used by a RL agent, which my peer wrote code for.

import copy

def runStudentDA(cur_context, input_desires, num_agents):
    '''
    Input: 
    cur_context is a list of the student RL agent's report of preferences.
    input_desires is a list of lists of all student and teacher's report preferences.
    num_agents is an integer of the number of agents

    This function runs the Student-Proposing Deferred Acceptance Algorithm.

    Output: 
    The agent's reward from their report of preferences after the matching algorithm has concluded.
    '''

    desires = copy.deepcopy(input_desires)
    desires[0] = cur_context

    print("Proposing preferences: ", desires[:num_agents])
    print("Accepting preferences: ", desires[num_agents:])
    print()

    student_preferences = copy.deepcopy(desires[:num_agents])
    teacher_preferences = desires[num_agents:]
    
    student_partners = [None] * num_agents
    teacher_partners = [None] * num_agents
    
    counter = 1
    while None in student_partners:

        # Step 1: All students ask their top preference remaining beta
        for student in range(0, num_agents):
            if student_partners[student] == None: # student is unassigned a teacher
                top_preference = student_preferences[student].pop(0)

                if top_preference == None:
                    # Student prefers themselves
                    student_partners[student] == -1
                    break

                # Step 2: All teachers accept their top preferred suitor, rejecting existing suitor
                # print("Student " + str(student)  + " proposes to Teacher " + str(top_preference))

                # If teacher accepts student's proposal
                if teacher_partners[top_preference] is None or (
                    # check that the student is strictly preferred to the existing partner
                    teacher_preferences[top_preference].index(student) <
                    teacher_preferences[top_preference].index(teacher_partners[top_preference])
                ):

                    # if teacher has a partner
                    if teacher_partners[top_preference]:
                        # print('Teacher ' + str(top_preference) + ' rejects  Student ' + str(teacher_partners[top_preference]))
                        student_partners[teacher_partners[top_preference]] = None
            
                    # log the match
                    # print('Teacher ' + str(top_preference) + ' accepts  Student ' + str(student))
                    student_partners[student] = top_preference
                    teacher_partners[top_preference] = student
                # else:
                    # print('Teacher ' + str(top_preference) + ' rejects  Student ' + str(student))
                    # move on to the next unmatched student
        
        print("Teacher-Proposing DA Round " + str(counter) + " results -- (student, teacher)")
        counter += 1
        for i in range(0, len(student_partners)):
            print("(" + str(i) + "," + str(student_partners[i]) + ")")

    print()
    print("Everyone is matched. This is a stable matching")

    # return score of Student 1's matching
    student_1_matched_teacher = student_partners[0]
    if student_1_matched_teacher == -1: # matched themselves
        return 0

    return num_agents - desires[:num_agents][0].index(student_1_matched_teacher)