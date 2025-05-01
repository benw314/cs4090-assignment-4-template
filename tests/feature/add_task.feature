Feature: Add tasks
  Scenario: User adds a new task
    Given there are no tasks
    When the user adds a task titled "Write report"
    Then the task list should contain a task titled "Write report"
