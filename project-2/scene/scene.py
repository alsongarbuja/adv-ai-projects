from pygame import Surface, Event

class SceneManager:
  """
  Class to act as the manager of all the screens in the game
  """
  def __init__(self):
    # Object of scene name and Scene (key-value pairs)
    self.scenes = {}
    # Object holding the current scene or None
    self.current_scene = None

  def add_scene(self, name, scene_obj):
    """
    Function to add scene into the scenes object

    Args:
      name: Name of the scene
      scene_obj: A Scene Object
    """
    self.scenes[name] = scene_obj

  def set_scene(self, name):
    """
    Function to set the scene to current scene

    Args:
      name: Name of the scene
    """
    self.current_scene = self.scenes.get(name)

  def handle_events(self, events: list[Event]):
    """
    Function to handle events if the current scene have events

    Args:
      events: List of pygame Events
    """
    if self.current_scene:
      self.current_scene.handle_events(events)

  def update(self):
    """
    Function to handle update in the current scene
    """
    if self.current_scene:
      self.current_scene.update()

  def draw(self, surface: Surface):
    """
    Function to handle drawing elements in scene in current scene

    Args:
      surface: A pygame Surface
      font: A pygame Font
    """
    if self.current_scene:
      self.current_scene.draw(surface)

class Scene:
  """
  Base class for scene
  """
  def __init__(self, manager):
    self.manager = manager

  def handle_events(self, events):
    pass

  def update(self):
    pass

  def draw(self, surface: Surface):
    pass
