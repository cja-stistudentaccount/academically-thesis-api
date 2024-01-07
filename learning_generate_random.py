import random

def generate_random_answers(question_choice_mapping):
    random_answers = {}
    
    for question, choices in question_choice_mapping.items():
        random_choice = random.choice(list(choices.keys()))
        random_answers[question] = choices[random_choice]
    
    return random_answers

# Example usage:
question_choice_mapping = {
        "When playing a brand new game, how do you learn the instructions?": {
            "I look for tutorials or guidance from someone else who has played": "Collaborative",
            "I read the instructions and rules to determine the objectives": "Independent",
            "I hop in and start playing and learn as I go": "Experiential",
            "I prefer a structured tutorial mode provided by the game": "Dependent"
        },
        "When faced with a complex problem or project, how do you typically approach it?": {
            "I collaborate with others to brainstorm ideas and work on solutions together.": "Collaborative",
            "I break down the problem, study relevant materials, and create a detailed plan of action.": "Independent",
            "I start working on the problem, experimenting with different approaches as I go.": "Experiential",
            "I seek detailed instructions and step-by-step guidance before starting": "Dependent"
        },
        "In a group setting, how do you contribute to discussions or projects?": {
            "I actively participate, share ideas, and seek input from others.": "Collaborative",
            "I prepare thoroughly before the meeting, presenting well-thought-out contributions.": "Independent",
            "I prefer to observe initially and then contribute based on the ongoing discussion.": "Adaptive",
            "I wait for others to take the lead and follow their instructions": "Dependent"
        },
        "When given a reading assignment, how do you approach it?": {
            "I discuss the material with classmates or a study group before delving into it.": "Collaborative",
            "I carefully read through the assigned material, taking notes to understand key concepts.": "Independent",
            "I start reading and learn as I go, occasionally referring to external resources.": "Experiential",
            "I rely on summary materials and study aids to understand the content": "Dependent"
        },
        "When preparing for a presentation, how do you organize your thoughts?": {
            "I collaborate with others to outline key points and gather diverse perspectives.": "Collaborative",
            "I create a structured outline and thoroughly research the topic independently.": "Independent",
            "I start building the presentation, refining and adjusting as I progress.": "Experiential",
            "I rely on predefined templates and guidelines for structuring my presentation": "Dependent"
        },
        "How do you manage your time when preparing for exams or assessments?": {
            "I create a study schedule and seek input from others on effective study strategies.": "Collaborative",
            "I follow a set routine, dedicating specific time to reading and understanding the material.": "Independent",
            "I adapt my study plan based on what seems most effective as I progress.": "Experiential",
            "I rely on pre-established study plans and schedules provided by others": "Dependent"
        },
        "When learning a new skill, such as a programming language or a musical instrument, what is your initial strategy?": {
            "I enroll in classes or seek guidance from experts to receive formal instruction.": "Collaborative",
            "I study the theory and principles before practicing and applying them.": "Independent",
            "I start experimenting and practicing right away, learning through hands-on experience.": "Experiential",
            "I prefer predefined exercises and step-by-step guides for learning": "Dependent"
        },
        "When faced with a difficult concept, what is your initial approach?": {
            "I seek out additional resources and explanations, including online tutorials or books.": "Collaborative",
            "I review the foundational material and work through examples to grasp the concept.": "Independent",
            "I experiment with different methods and problem-solving strategies until I understand.": "Experiential",
            "I rely on explicit solutions and detailed explanations provided by others": "Dependent"
        },
        "How do you typically organize your study environment?": {
            "I prefer studying in groups or collaborative spaces with peers.": "Collaborative",
            "I create a quiet and organized space with all necessary materials for focused individual study.": "Independent",
            "I adapt my study environment based on the task, sometimes studying in different places.": "Adaptive",
            "I follow predefined study environments and setups recommended by others": "Dependent"
        },
        "When preparing for an exam, what is your preferred method of review?": {
            "I participate in study groups or review sessions with classmates.": "Collaborative",
            "I create a detailed study guide and review notes and textbooks thoroughly.": "Independent",
            "I quiz myself on the material and focus on areas where I feel less confident.": "Experiential",
            "I rely on practice exams and materials provided by others": "Dependent"
        },
        "When introduced to a new technology or software, how do you learn to use it?": {
            "I seek help from knowledgeable individuals or attend training sessions.": "Collaborative",
            "I read the user manual and follow instructions to understand the features and functions.": "Independent",
            "I explore the software on my own, experimenting with different features as I go.": "Experiential",
            "I rely on predefined guides and tutorials for using the technology": "Dependent"
        },
        "How do you handle distractions while studying or working on a project?": {
            "I find it helpful to have others around to keep me focused and on track.": "Collaborative",
            "I create a distraction-free zone and set specific time blocks for focused work.": "Independent",
            "I adapt to distractions, finding ways to work effectively even in a less controlled environment.": "Adaptive",
            "I rely on external systems or tools to minimize distractions": "Dependent"
        },
        "When assigned a group project, how do you approach collaboration with team members?": {
            "I actively participate in team meetings, contributing ideas and seeking input from others.": "Collaborative",
            "I assign specific tasks based on individual strengths and coordinate the overall project.": "Independent",
            "I adapt my role based on the team's needs, taking on various responsibilities as necessary.": "Adaptive",
            "I follow predefined roles and instructions provided by others": "Dependent"
        },
        "When given a choice between multiple study materials, how do you decide what to use?": {
            "I consult with peers or instructors to gather recommendations on the most effective materials.": "Collaborative",
            "I carefully review each material, considering its content, relevance, and potential benefits.": "Independent",
            "I sample different materials and adapt my study approach based on what works best for me.": "Experiential",
            "I rely on recommended study materials and guides provided by others": "Dependent"
        },
        "How do you approach learning a new physical skill, such as a sport or a musical instrument?": {
            "I take lessons from an instructor or coach to receive formal guidance.": "Collaborative",
            "I study the fundamental principles and techniques before practicing extensively.": "Independent",
            "I jump into practice, refining my skills through trial and error as I go.": "Experiential",
            "I follow predefined training programs and exercises provided by others": "Dependent"
        },
        "When faced with a large amount of information to learn, how do you organize it for better understanding?": {
            "I discuss the material with others to gain different perspectives and insights.": "Collaborative",
            "I create an organized outline or mind map to visually represent the information.": "Independent",
            "I start studying and adapt my approach based on what seems most effective as I progress.": "Adaptive",
            "I rely on predefined summaries and structures provided by others": "Dependent"
        },
        "When faced with a difficult assignment, how do you manage your time to complete it successfully?": {
            "I seek assistance from peers or instructors to break down the assignment and get guidance.": "Collaborative",
            "I carefully plan out each step of the assignment and follow a structured timeline.": "Independent",
            "I start working on the assignment, adjusting my approach based on progress and challenges.": "Adaptive",
            "I follow predefined guidelines and timelines provided by others": "Dependent"
        },
        "When learning from online resources, how do you ensure understanding and retention of the material?": {
            "I participate in online forums or discussion groups to share insights and ask questions.": "Collaborative",
            "I take detailed notes while watching or reading online content to reinforce understanding.": "Independent",
            "I engage with the material actively, experimenting with concepts and applying them in practical scenarios.": "Experiential",
            "I follow predefined online learning structures and activities provided by others": "Dependent"
        }
        # Add mappings for any additional questions...
    }

random_answers = generate_random_answers(question_choice_mapping)
print(random_answers)
