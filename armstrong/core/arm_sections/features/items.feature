Feature: Retrieving Items for Section
  In order to access all of the items associated with a Section
  I need to be able to retrieve the items that are related to a Section

  Scenario: Using common model backend
    Given I have a "Common" model registered with the backends
    And I have the following Sections:
      | title   | slug      | summary           |
      | Local   | local     | All about local   |
      | Sports  | sports    | All about sports  |
      | Weather | weather   | All about weather |
    And I have the following many-to-many models from support app:
      | model   | title                         | sections|
      | Article | Baseball dunks basket         | sports  |
      | Article | Basketball team hits home run | sports  |
      | Photo   | Football team sinks 30' putt  | sports  |
    When I query for a section by slug "sports/"
    And I load the section's items
    Then I should have the following model:
      | model   | title                         |
      | Article | Baseball dunks basket         |
      | Article | Basketball team hits home run |
      | Photo   | Football team sinks 30' putt  |

  Scenario: Basic backend works with regular manager
    Given I have a "SimpleCommon" model registered with the backends
    And I have the following Sections:
      | title   | slug      | summary           |
      | Local   | local     | All about local   |
      | Sports  | sports    | All about sports  |
      | Weather | weather   | All about weather |
    And I have the following models from support app:
      | model         | title                          | section |
      | SimpleArticle | Baseball dunks basket          | sports  |
      | SimpleArticle | Basketball team hits home run  | sports  |
      | SimplePhoto   | Football team sinks 30' putt   | sports  |
      | SimpleArticle | Local mayor voted best citizen | local   |
    When I query for a section by slug "sports/"
    And I load the section's items
    Then I should have the following model:
      | model        | title                         |
      | SimpleCommon | Baseball dunks basket         |
      | SimpleCommon | Basketball team hits home run |
      | SimpleCommon | Football team sinks 30' putt  |

  Scenario: Basic backend works with non-standard field name
    Given I have a "NonStandardField" model registered with the backends
    And I have the following Sections:
      | title   | slug      | summary           |
      | Local   | local     | All about local   |
      | Sports  | sports    | All about sports  |
      | Weather | weather   | All about weather |
    And I have the following models from support app:
      | model            | title             | section |
      | NonStandardField | Some random title | sports  |
    When I query for a section by slug "sports/"
    And I load the section's items
    Then I should have the following model:
      | model            | title             |
      | NonStandardField | Some random title |

  Scenario: Uses backends to get items
    Given I have a "NonStandardField" model registered with the backends
    And I have the following Sections:
      | title   | slug      | summary           |
      | Sports  | sports    | All about sports  |
    And I have a fake backend configured for items
    When I query for a section by slug "sports/"
    And I load the section's items
    Then the fake backend should have been called
