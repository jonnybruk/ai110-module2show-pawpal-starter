# PawPal+ Project Reflection

## 1. System Design

- Track pet care tasks, Consider constraints, Produce a daily plan and explain why it chose that plan

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
Owner - Represents the user of the app and store basic info and manage a list of pets.

Pet - Represents one animal and holds pet details and the list of care tasks for that pet.

Task - Represents a single care activity and stores task info (type, duration, priority, due time) and track completion.

Constraint - Represents the owner’s limits for the day and stores available time and preferences, and check whether tasks fit those limits.

DailyPlanner - The decision‑maker of the system and rank tasks, choose which ones fit the day’s constraints, and explain why they were selected or skipped.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Replaced Constraint and DailyPlanner with Scheduler to simplify things.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)? time and pet associations
- How did you decide which constraints mattered most? time mattered most to ensure chronological routine

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes. it checks for time overlaps rather than duration-based conflicts
- Why is that tradeoff reasonable for this scenario? exact time matching is simple to implement and cover the most common errors w/o needing complex time block logic

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)? for brainstorming, generating pytest functions, and refactoring
- What kinds of prompts or questions were most helpful? "how do I check if an object exists in st.session_state?"

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is. when AI suggested to use a complex database early on
- How did you evaluate or verify what the AI suggested? by running pytest

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test? task completion and pet-association
- Why were these tests important? they ensured data isn't lost during the bridge between backend logic and streamlit UI

**b. Confidence**

- How confident are you that your scheduler works correctly? 5/5
- What edge cases would you test next if you had more time? overlapping tasks

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with? integrating scheduler class w/ streamlit UI

**b. What you would improve**

- If you had another iteration, what would you improve or redesign? i would redesign the "Task" class to include categories and add a calendar view

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project? AI is a powerful tool for syntax but the human architect must define the logic and constraints to keep the project on track.
