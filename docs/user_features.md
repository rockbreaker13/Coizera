# Coizera Gherkin Use Cases

This document contains Gherkin use cases for the user features of the Coizera game.

## Player

### Player Movement

**Feature:** Player can move within the game world.

  **Scenario:** Player moves up
    Given the player is in the game world
    When the player presses the "W" key
    Then the player's vertical position should decrease

  **Scenario:** Player moves down
    Given the player is in the game world
    When the player presses the "S" key
    Then the player's vertical position should increase

  **Scenario:** Player moves left
    Given the player is in the game world
    When the player presses the "A" key
    Then the player's horizontal position should decrease

  **Scenario:** Player moves right
    Given the player is in the game world
    When the player presses the "D" key
    Then the player's horizontal position should increase

### Weapon Management

**Feature:** Player can manage and switch weapons.

  **Scenario:** Player switches to the first weapon
    Given the player has at least one weapon
    When the player presses the "1" key
    Then the player should be holding the first weapon

  **Scenario:** Player switches to the second weapon
    Given the player has at least two weapons
    When the player presses the "2" key
    Then the player should be holding the second weapon

### Health and Damage

**Feature:** Player's health changes based on game events.

  **Scenario:** Player takes damage
    Given the player has 20 HP
    When the player takes 5 damage
    Then the player's HP should be 15

  **Scenario:** Player regenerates health
    Given the player has 10 HP and has not been attacked recently
    When time passes
    Then the player's HP should increase

  **Scenario:** Player dies
    Given the player has 5 HP
    When the player takes 5 or more damage
    Then the player's state should be "dead"

### Zone Boundaries

**Feature:** Player is confined to the current zone.

  **Scenario:** Player hits the left boundary in the base zone
    Given the player is in the "base" zone
    When the player moves to the left edge of the screen
    Then the player should not be able to move further left

  **Scenario:** Player hits the right boundary in the forest zone
    Given the player is in the "forest" zone
    When the player moves to the right edge of the screen
    Then the player should not be able to move further right

## Items

### Item Lifecycle

**Feature:** Items appear, can be collected, and disappear in the game world.

  **Scenario:** An item spawns in the world
    Given the game is running
    When an item is created
    Then it should appear with a dropping animation

  **Scenario:** Player collects an item
    Given an item exists near the player
    When the player moves close to the item
    Then the item should move towards the player and disappear

  **Scenario:** An item despawns
    Given an item has been in the world for a long time
    When the despawn timer is reached
    Then the item should fade out and be removed

### Item Types

**Feature:** Different types of items can exist in the game.

  **Scenario:** A stick is in the game
    Given a "Stick" item exists
    Then it should be identifiable as a stick

  **Scenario:** A rock is in the game
    Given a "Rock" item exists
    Then it should be identifiable as a rock

## Weapon

### Weapon Usage

**Feature:** Player can use weapons to attack.

  **Scenario:** Player swings a weapon
    Given the player has a weapon equipped
    When the player clicks the left mouse button
    Then the weapon should perform a swinging animation

  **Scenario:** Weapon is aimed at the cursor
    Given the player is holding a weapon
    When the player moves the mouse
    Then the weapon should be aimed towards the cursor's position

  **Scenario:** Weapon swing creates a trail
    Given the player swings a weapon
    When the weapon is in motion
    Then a visual trail effect should be displayed

### Weapon Properties

**Feature:** Weapons have different properties and effects.

  **Scenario:** Equipped weapon determines player damage
    Given the player equips a weapon with 10 damage
    Then the player's damage stat should be 10

  **Scenario:** Some weapons have special effects
    Given the player equips a weapon with a "speed" effect
    Then the weapon's swing speed should be faster than normal

  **Scenario:** Specific weapons fire projectiles
    Given the player is holding the "Inferno" weapon
    When the player attacks
    Then fire projectiles should be launched

## Enemies

### Enemy Behavior

**Feature:** Enemies interact with the player.

  **Scenario:** Enemy moves towards the player
    Given an enemy is in the game world
    When the player is within the enemy's range
    Then the enemy should move towards the player

  **Scenario:** Enemy damages the player
    Given an enemy is next to the player
    When the enemy touches the player
    Then the player's health should decrease

  **Scenario:** Player damages an enemy
    Given an enemy has 10 HP
    When the player hits the enemy with a weapon that deals 5 damage
    Then the enemy's HP should be 5

  **Scenario:** Enemy dies and drops loot
    Given an enemy has 5 HP
    When the player deals 5 or more damage to the enemy
    Then the enemy should be removed from the game and drop items

### Enemy Types

**Feature:** Different types of enemies with unique characteristics.

  **Scenario:** A Bouncing Slime is in the game
    Given a "BouncingSlime" enemy exists
    Then it should move with a hopping motion

  **Scenario:** A Shadow Stalker is in the game
    Given a "ShadowStalker" enemy exists far from the player
    Then it should be nearly invisible
    When the player gets closer to the "ShadowStalker"
    Then it should become more visible

  **Scenario:** A Magma Slime is in the game
    Given a "MagmaSlime" enemy exists
    When it moves
    Then it should leave a trail of smoke and sparks

## Buildings

### Crafting and Interaction

**Feature:** Player can use buildings to craft items and travel.

  **Scenario:** Player opens a crafting menu
    Given a "Crafting Table" is in the game world
    When the player clicks on the "Crafting Table"
    Then the crafting menu should be displayed

  **Scenario:** Player crafts an item
    Given the player has the required ingredients for a "Pickaxe"
    And the crafting menu is open
    When the player clicks on the "Pickaxe" recipe
    Then the ingredients should be removed from the player's inventory
    And a "Pickaxe" should be added to the player's items

  **Scenario:** Furnace requires fuel
    Given the player is using a "Furnace"
    And the furnace has no fuel
    When the player tries to craft an item
    Then the crafting should fail
    When the player adds "Coal" to the furnace
    Then the furnace should become active

  **Scenario:** Player uses a ladder to change zones
    Given the player is standing on a "MineLadder"
    When the player activates the ladder
    Then the player should be transported to the "mine1" zone

## Game Events and Feedback

### Player and World Feedback

**Feature:** The game provides feedback to the player through events.

  **Scenario:** Player taking damage is communicated
    Given the player is in the game
    When an enemy attacks the player
    Then a "PlayerTakesDamage" event should occur

  **Scenario:** Item pickup is communicated
    Given the player is near an item
    When the player collects the item
    Then a "PlayerPicksUpItem" event should occur

  **Scenario:** Screen shakes for impact
    Given the player is in the game
    When a significant event like an explosion happens
    Then a "ScreenShake" event should occur, shaking the screen
