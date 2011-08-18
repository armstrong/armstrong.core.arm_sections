Feature: Getting models with full slug
  In order to be able to query for an item in a Section
  As a developer
  I want to have access to a manager that can build the correct query for me

  Scenario: Basic loading
    Given I have a "Common" model registered with the backends
    And I have the following Sections:
      | title   | slug      | summary           |
      | Local   | local     | All about local   |
      | Sports  | sports    | All about sports  |
      | Weather | weather   | All about weather |
    And I have the following many-to-many models from support app:
      | model   | title                         | sections| slug            |
      | Article | Baseball dunks basket         | sports  | baseball-team   |
      | Article | Basketball team hits home run | sports  | basketball-team |
      | Photo   | Football team sinks 30' putt  | sports  | football-team   |
    When I query "Common" with the full slug "sports/football-team"
    Then I should have the following model:
      | model   | title                         |
      | Photo   | Football team sinks 30' putt  |

  Scenario: Works with trailing slash
    Given I have a "Common" model registered with the backends
    And I have the following Sections:
      | title   | slug      | summary           |
      | Local   | local     | All about local   |
      | Sports  | sports    | All about sports  |
      | Weather | weather   | All about weather |
    And I have the following many-to-many models from support app:
      | model   | title                         | sections| slug            |
      | Article | Baseball dunks basket         | sports  | baseball-team   |
      | Article | Basketball team hits home run | sports  | basketball-team |
      | Photo   | Football team sinks 30' putt  | sports  | football-team   |
    When I query "Common" with the full slug "sports/football-team/"
    Then I should have the following model:
      | model   | title                         |
      | Photo   | Football team sinks 30' putt  |

  Scenario: Works with leading slash
    Given I have a "Common" model registered with the backends
    And I have the following Sections:
      | title   | slug      | summary           |
      | Local   | local     | All about local   |
      | Sports  | sports    | All about sports  |
      | Weather | weather   | All about weather |
    And I have the following many-to-many models from support app:
      | model   | title                         | sections| slug            |
      | Article | Baseball dunks basket         | sports  | baseball-team   |
      | Article | Basketball team hits home run | sports  | basketball-team |
      | Photo   | Football team sinks 30' putt  | sports  | football-team   |
    When I query "Common" with the full slug "/sports/football-team"
    Then I should have the following model:
      | model   | title                         |
      | Photo   | Football team sinks 30' putt  |

  Scenario: Works with non-inheritence enabled QuerySets
    Given I have a "SimpleCommon" model registered with the backends
    And I have the following Sections:
      | title   | slug      | summary           |
      | Local   | local     | All about local   |
      | Sports  | sports    | All about sports  |
      | Weather | weather   | All about weather |
    And I have the following models from support app:
      | model         | title                         | section | slug            |
      | SimpleArticle | Baseball dunks basket         | sports  | baseball-team   |
      | SimpleArticle | Basketball team hits home run | sports  | basketball-team |
      | SimplePhoto   | Football team sinks 30' putt  | sports  | football-team   |
    When I query "SimpleCommon" with the full slug "sports/football-team"
    Then I should have the following model:
      | model        | title                        |
      | SimpleCommon | Football team sinks 30' putt |

  Scenario: Raises DoesNotExist on not-found
    Given I have a "Common" model registered with the backends
    And I have the following Sections:
      | title   | slug      | summary           |
      | Local   | local     | All about local   |
      | Sports  | sports    | All about sports  |
      | Weather | weather   | All about weather |
    And I have the following many-to-many models from support app:
      | model   | title                         | sections| slug            |
      | Article | Baseball dunks basket         | sports  | baseball-team   |
      | Article | Basketball team hits home run | sports  | basketball-team |
      | Photo   | Football team sinks 30' putt  | sports  | football-team   |
    When I query "Common" with the full slug "unknown/and/unknowable"
    Then I should have caught a "DoesNotExist" exception

  Scenario: Works with non-standard field names
    Given I have a "Common" model registered with the backends
    And I have the following Sections:
      | title   | slug      | summary           |
      | Local   | local     | All about local   |
      | Sports  | sports    | All about sports  |
      | Weather | weather   | All about weather |
    And I have the following NonStandardField models:
      | title                         | section | slug            |
      | Baseball dunks basket         | sports  | baseball-team   |
      | Basketball team hits home run | sports  | basketball-team |
      | Football team sinks 30' putt  | sports  | football-team   |
    When I query "NonStandardField" with the full slug "sports/football-team"
    Then I should have the following model:
      | model            | title                        |
      | NonStandardField | Football team sinks 30' putt |
