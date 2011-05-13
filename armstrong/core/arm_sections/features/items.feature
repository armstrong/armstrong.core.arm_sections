Feature: Retrieving Items for Section
  In order to access all of the items associated with a Section
  I need to be able to retrieve the items that are related to a Section

  Scenario: Using common model backend
    Given I have a Common model registered with the backends
    And I have the following Sections:
      | title   | slug      | summary           |
      | Local   | local     | All about local   |
      | Sports  | sports    | All about sports  |
      | Weather | weather   | All about weather |
    And I have the following models from support app:
      | model   | title                         |
      | Article | Baseball dunks basket         |
      | Article | Basketball team hits home run |
      | Photo   | Football team sinks 30' putt  |
    When I query for a section by slug "sports/"
    And I load the section's items
    Then I should have the following model:
      | model   | title                         |
      | Article | Baseball dunks basket         |
      | Article | Basketball team hits home run |
      | Photo   | Football team sinks 30' putt  |
