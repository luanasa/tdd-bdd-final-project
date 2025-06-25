Feature: Product Catalog Service
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name       | description          | price   | available | category   |
        | Hat        | A red fedora         | 59.95   | True      | CLOTHING   |
        | Shoes      | Blue running shoes   | 120.50  | False     | CLOTHING   |
        | Big Mac    | 1/4 lb burger        | 5.99    | True      | FOOD       |
        | Sheets     | Queen bed sheets     | 87.00   | True      | HOMEGOODS  |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Catalog Administration" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hammer"
    And I set the "Description" to "Claw hammer"
    And I select "True" in the "Available" dropdown
    And I select "TOOLS" in the "Category" dropdown
    And I set the "Price" to "34.95"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Description" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Hammer" in the "Name" field
    And I should see "Claw hammer" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "TOOLS" in the "Category" dropdown
    And I should see "34.95" in the "Price" field

Scenario: Read a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Hat" in the "Name" field
    And I should see "A red fedora" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "CLOTHING" in the "Category" dropdown
    And I should see "59.95" in the "Price" field

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "Shoes"
    And I press the "Search" button
    Then I should see the message "Success"
    And I change the "Name" to "Running Shoes"
    And I change the "Price" to "135.00"
    And I change the "Available" to "True"
    And I press the "Update" button
    Then I should see the message "Success"
    And I should see "Running Shoes" in the "Name" field
    And I should see "135.00" in the "Price" field
    And I should see "True" in the "Available" dropdown

Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Name" to "Big Mac"
    And I press the "Search" button
    Then I should see the message "Success"
    When I press the "Delete" button
    Then I should see the message "Success"
    And I should not see "Big Mac" in the search results

Scenario: List all Products
    When I visit the "Home Page"
    And I press the "List All" button
    Then I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results

Scenario: Search Products by Category
    When I visit the "Home Page"
    And I select "CLOTHING" in the "Category" dropdown
    And I press the "Search" button
    Then I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should not see "Big Mac" in the results
    And I should not see "Sheets" in the results

Scenario: Search Products by Availability
    When I visit the "Home Page"
    And I select "True" in the "Available" dropdown
    And I press the "Search" button
    Then I should see "Hat" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results
    And I should not see "Shoes" in the results

Scenario: Search Products by Name
    When I visit the "Home Page"
    And I set the "Name" to "She"
    And I press the "Search" button
    Then I should see "Sheets" in the results
    And I should not see "Hat" in the results
    And I should not see "Shoes" in the results
    And I should not see "Big Mac" in the results