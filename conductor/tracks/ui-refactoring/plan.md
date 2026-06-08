# Plan: Refactor UI Elements into Components

This plan outlines the process of refactoring the Coizera game's UI into a component-based system using `pygame.sprite.Sprite` and the existing `pubsub` system for events.

## Tasks

1.  [x] Set up Conductor track.
2.  [ ] Analyze the codebase to identify UI elements for refactoring.
3.  [ ] Create `ui.py` and implement the `LabeledButton` component.
4.  [ ] Integrate `LabeledButton` with the `pubsub` system.
5.  [ ] Refactor the `CraftingTable` menu to use `LabeledButton`.
6.  [ ] Wire up `LabeledButton` events for the `CraftingTable`.
7.  [ ] Review and finalize the UI refactoring.
