Feature: Basic Sections
  In order to provide a hierarchy of Sections within a Site
  As a Developer
  I need access to a Section model

  Scenario: Retrieval by slug
    Given I have the following Sections:
      | title   | slug      | summary           |
      | Local   | local     | All about local   |
      | Sports  | sports    | All about sports  |
      | Weather | weather   | All about weather |
    When I query for a Section by slug "sports"
    Then I should have a Section with the following fields:
      | title   | slug      | summary           |
      | Sports  | sports    | All about sports  |

  Scenario: Retrieve children by slug
    Given I have the following Sections:
      | title   | slug      | summary                   | parent__slug |
      | Local   | local     | All about local           | None         |
      | Sports  | sports    | All about sports          | None         |
      | College | college   | All about college sports  | sports       |
      | Pro     | pro       | All about pro sports      | sports       |
      | Weather | weather   | All about weather         | None         |
    When I query for a section by slug "sports/pro"
    Then I should have a Section with the following fields:
      | title   | slug      | summary                   | parent__slug |
      | Pro     | pro       | All about pro sports      | sports       |

  Scenario: Figuring out the parent
    Given I have the following Sections:
      | title   | slug      | summary                   | parent__slug |
      | Local   | local     | All about local           | None         |
      | Sports  | sports    | All about sports          | None         |
      | College | college   | All about college sports  | sports       |
      | Pro     | pro       | All about pro sports      | sports       |
      | Weather | weather   | All about weather         | None         |
    And I query for a section by slug "sports/pro"
    When I retrieve the section's parent
    Then I should have a Section with the following fields:
      | title   | slug      | summary                   | parent__slug |
      | Sports  | sports    | All about sports          | None         |

  Scenario: Retrieving all of the children for a Section
    Given I have the following Sections:
      | title     | slug    | summary                    | parent__slug |
      | Local     | local   | All about local            | None         |
      | Sports    | sports  | All about sports           | None         |
      | College   | college | All about college sports   | sports       |
      | Texas     | texas   | All about Texas sports     | college      |
      | Texas A&M | a-m     | All about Texas A&M sports | college      |
      | Pro       | pro     | All about pro sports       | sports       |
      | Weather   | weather | All about weather          | None         |
    And I query for a section by slug "sports"
    When I start monitoring the number of queries run
    And I retrieve the children
    Then I should have the following sections:
      | title     | slug    | summary                    |
      | College   | college | All about college sports   |
      | Texas     | texas   | All about Texas sports     |
      | Texas A&M | a-m     | All about Texas A&M sports |
      | Pro       | pro     | All about pro sports       |
    And only 1 query should have been run
