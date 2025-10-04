# Jarvis Task Management System

## Overview
The enhanced Task Management System for Jarvis provides comprehensive voice-controlled task organization, tracking, and productivity features. Users can create, manage, and track tasks using natural language voice commands.

## Features

### ✅ Core Task Management
- **Add Tasks**: Create tasks with descriptions, deadlines, and priorities
- **Complete Tasks**: Mark tasks as completed via voice commands
- **Delete Tasks**: Remove tasks from the system
- **Search Tasks**: Find tasks by keywords
- **List Tasks**: View tasks by time period (today, week, all)

### ✅ Advanced Organization
- **Priority Levels**: High, Normal, Low priority tasks
- **Categories**: Organize tasks into custom categories
- **Deadlines**: Natural language deadline parsing
- **Statistics**: Track productivity and completion rates

### ✅ Smart Features
- **Overdue Detection**: Automatically identify overdue tasks
- **Reminders**: Set custom reminders for tasks
- **Daily Summaries**: Get comprehensive daily task overviews
- **Help System**: Built-in help for all commands

## Voice Commands

### Adding Tasks
```
"Add task: [description]"
"Add urgent task: [description]"
"Create task: [description] by [deadline]"
"New task: [description] at [time]"
```

**Examples:**
- "Add task: Buy groceries"
- "Add urgent task: Call mom by 5 PM today"
- "Create task: Submit assignment by Friday"
- "New task: Doctor appointment at 2:30 PM tomorrow"

### Managing Tasks
```
"What are my tasks today?"
"Show today's tasks"
"What are my tasks this week?"
"Show this week's tasks"
"List all tasks"
"Show overdue tasks"
```

### Completing Tasks
```
"Mark task completed: [task name]"
"Complete task: [task name]"
"Task completed: [task name]"
"Done with task: [task name]"
"Finish task: [task name]"
```

### Task Organization
```
"Set task priority: [task name] to [high/normal/low]"
"Add task category: [task name] to [category]"
"Show tasks by category: [category]"
"List categories"
```

### Searching and Statistics
```
"Search tasks: [search term]"
"Find task: [search term]"
"Task statistics"
"Task stats"
"Daily summary"
"Task summary"
```

### Deleting Tasks
```
"Delete task: [task name]"
```

### Reminders
```
"Set task reminder: [task name] in [X] minutes"
"What tasks need reminders?"
"Tasks needing reminders"
```

### Help
```
"Task help"
"Help with tasks"
"Task management help"
"How to use tasks"
```

## Deadline Formats

The system supports various natural language deadline formats:

### Time References
- "today", "tomorrow", "day after tomorrow"
- "this week", "next week", "this weekend"
- "next month", "next year"

### Weekdays
- "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
- "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"

### Specific Times
- "5 PM", "2:30 AM", "8:00 PM"
- "17:30", "14:30" (24-hour format)
- "8am", "5pm"

### Date Formats
- "12/25", "25/12" (MM/DD or DD/MM)
- "12-25", "25-12" (MM-DD or DD-MM)
- "12.25", "25.12" (MM.DD or DD.MM)

### Combined Examples
- "by 5 PM today"
- "before Friday"
- "at 2:30 PM tomorrow"
- "on Monday"
- "next week"
- "this weekend"

## Data Storage

Tasks are stored in JSON format in `data/tasks.json` with the following structure:

```json
{
  "id": 1234567890123,
  "title": "Task description",
  "priority": "high|normal|low",
  "deadline": "2024-01-15T17:00:00",
  "completed": false,
  "created_at": "2024-01-15T10:00:00",
  "completed_at": null,
  "category": "work",
  "reminder_set": true,
  "reminder_minutes": 30
}
```

## Integration

The task management system integrates seamlessly with:
- **Voice Recognition**: All commands work through speech
- **Text-to-Speech**: Responses are spoken back to the user
- **Reminder System**: Tasks can trigger automatic reminders
- **Statistics Tracking**: Productivity insights and completion rates

## Error Handling

The system includes comprehensive error handling:
- Input validation for all commands
- Graceful handling of missing tasks
- Clear error messages via voice
- Fallback suggestions for unclear commands

## Getting Started

1. **Wake up Jarvis**: Say "Wake up" to start the system
2. **Add your first task**: "Add task: [description]"
3. **Check your tasks**: "What are my tasks today?"
4. **Get help**: "Task help" for a complete command list

## Tips for Best Results

1. **Be specific**: Use clear, descriptive task names
2. **Set deadlines**: Include time references for better organization
3. **Use categories**: Group related tasks together
4. **Check regularly**: Use daily summaries to stay on track
5. **Complete tasks**: Mark tasks as done to maintain accurate statistics

## Troubleshooting

- **Task not found**: Check the exact spelling of the task name
- **Deadline not recognized**: Try simpler time formats like "5 PM today"
- **No response**: Ensure Jarvis is listening and try again
- **Help needed**: Say "Task help" for command assistance

---

The Task Management System transforms Jarvis into a powerful productivity assistant, helping users stay organized and on track with their daily tasks and goals.
