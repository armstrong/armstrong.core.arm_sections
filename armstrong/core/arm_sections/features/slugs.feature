Feature: Handling of slugs
  In order to keep from destroying the database
  I need the ability to query for the full hierarchy of slugs simply

  Scenario: Querying with a trailing slash in slug
    Given I have the following Sections:
      | title   | slug      | summary                   | parent__slug |
      | Local   | local     | All about local           | None         |
      | Sports  | sports    | All about sports          | None         |
      | College | college   | All about college sports  | sports       |
      | Pro     | pro       | All about pro sports      | sports       |
      | Weather | weather   | All about weather         | None         |
    When I start monitoring the number of queries run
    And I query for a section by slug "sports/"
    Then I should have a Section with the following fields:
      | title   | slug      | summary                   | parent__slug |
      | Sports  | sports    | All about sports          | None         |


  Scenario: Querying for a child
    Given I have the following Sections:
      | title   | slug      | summary                   | parent__slug |
      | Local   | local     | All about local           | None         |
      | Sports  | sports    | All about sports          | None         |
      | College | college   | All about college sports  | sports       |
      | Pro     | pro       | All about pro sports      | sports       |
      | Weather | weather   | All about weather         | None         |
    When I start monitoring the number of queries run
    And I query for a section by slug "sports/pro"
    Then only 1 query should have been run

  Scenario: Querying for a grand-child
    Given I have the following Sections:
      | title     | slug    | summary                    | parent__slug |
      | Local     | local   | All about local            | None         |
      | Sports    | sports  | All about sports           | None         |
      | College   | college | All about college sports   | sports       |
      | Texas     | texas   | All about Texas sports     | college      |
      | Texas A&M | a-m     | All about Texas A&M sports | college      |
      | Pro       | pro     | All about pro sports       | sports       |
      | Weather   | weather | All about weather          | None         |
    When I start monitoring the number of queries run
    And I query for a section by slug "sports/college/texas/"
    Then only 1 query should have been run

  Scenario: Changing a parent
    Given I have the following Sections:
      | title     | slug    | summary                    | parent__slug |
      | Local     | local   | All about local            | None         |
      | Sports    | sports  | All about sports           | None         |
      | College   | college | All about college sports   | sports       |
      | Texas     | texas   | All about Texas sports     | college      |
      | Texas A&M | a-m     | All about Texas A&M sports | college      |
      | Pro       | pro     | All about pro sports       | sports       |
      | Weather   | weather | All about weather          | None         |
    When I query for a Section by slug "sports"
    And I change the slug to "all-sports"
    And I load all sections
    Then I should have the following sections:
      | title     | slug       | summary                    | full_slug                 |
      | Local     | local      | All about local            | local/                    |
      | Sports    | all-sports | All about sports           | all-sports/               |
      | College   | college    | All about college sports   | all-sports/college/       |
      | Texas     | texas      | All about Texas sports     | all-sports/college/texas/ |
      | Texas A&M | a-m        | All about Texas A&M sports | all-sports/college/a-m/   |
      | Pro       | pro        | All about pro sports       | all-sports/pro/           |
      | Weather   | weather    | All about weather          | weather/                  |
