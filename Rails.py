import sublime, sublime_plugin, os, glob, re
from vendor.inflector import *

# @author Luqman Amjad http://luqmanamjad.com

# Taken from Git Plugin (Changed to detected Rails root)
def rails_root(directory):
  while directory:
    if os.path.exists(os.path.join(directory, 'Rakefile')):
      return directory
    parent = os.path.realpath(os.path.join(directory, os.path.pardir))
    if parent == directory:
      # /.. == /
      return False
    directory = parent
  return False

class RailsRelatedFilesHelper:

  @staticmethod
  def get_directory_listing_without_folders(path):

    files = []
    result = glob.glob(path)

    for _file in result:

      if not os.path.isdir(_file):
        files.append(_file)

    return files

  @staticmethod
  def for_controllers(app_folder, working_directory, base_file_name):

    controller = base_file_name.replace('_controller', '')
    model = Inflector(English).singularize(controller).lower()

    namespace_directory    = RailsRelatedFilesHelper.get_namespace_directory(working_directory)
    working_directory_base = os.path.basename(working_directory)

    if namespace_directory:
      
      controller = os.path.join(working_directory_base, controller)

    walkers = [
      'models/'  + model      + '*',   # Models
      'helpers/' + model      + '**'   # Helpers
      'views/'   + controller + '/**'  # Views
    ]

    return RailsRelatedFilesHelper.get_files_while_walking(app_folder, walkers)

  @staticmethod
  def for_views(app_folder, working_directory):
 
    working_directory_base = os.path.basename(working_directory) #if app/views/posts it should return "posts"
    model                  = Inflector(English).singularize(os.path.basename(working_directory_base)).lower() # should return "post"
    namespace_directory    = RailsRelatedFilesHelper.get_namespace_directory(working_directory) #should return none
    controller = model

    if namespace_directory:
      working_directory_base = namespace_directory

      controller = os.path.join(os.path.split(working_directory_base)[0], controller)

    walkers = [
      'models/'             + model + '**',
      'views/'              + working_directory_base + '/**',
      'helpers/'            + model + '**',
      'assets/javascripts/' + model + '**',
      'assets/stylesheets/' + model + '**',
      'controllers/'        + controller + '**'
    ]
    
    return RailsRelatedFilesHelper.get_files_while_walking(app_folder, walkers)
  
  @staticmethod
  def for_models(app_folder, working_directory, file_name_base_no_ext):

    model = Inflector(English).singularize(file_name_base_no_ext).lower()
    controller = Inflector(English).pluralize(file_name_base_no_ext).lower()
    
    walkers = [
      'models/'         + model      + '**',
      'helpers/'        + model      + '**',  # Helpers
      'views/'          + controller + '/**', # Views
      'views/**/'       + controller + '/**',  # Views
      'controllers/'    + controller + '**',  # Controllers looks under controllers/model** 
      'controllers/**/' + controller + '**',  # Controllers looks under controllers/**sub directories**/model**
    ]

    return RailsRelatedFilesHelper.get_files_while_walking(app_folder, walkers)

  @staticmethod
  def get_app_sub_directory(filename):

    regex = re.compile('(views|controllers|helpers|models|assets)')
    match = regex.findall(filename)

    if match:

      return match[0]

    else:

      return

  @staticmethod
  def get_namespace_directory(directory):

    regex = re.compile('(\/app\/views|controllers)\/(.*)') #amazing regex skills...
    match = regex.findall(directory)

    if match:

      return match[0][1]

    else:

      return

  @staticmethod
  def get_files_while_walking(app_folder, walkers):

    files = []
      
    for walker in walkers:

      files += (
        RailsRelatedFilesHelper().get_directory_listing_without_folders(app_folder + '/' + walker)
      )

    files_without_full_path = []
    for _file in files:

      files_without_full_path += [_file.replace(app_folder + '/', 'app/')]

    return files_without_full_path

class RailsRelatedFilesCommand(sublime_plugin.TextCommand):
  
  APP_FOLDERS = ['controllers', 'models', 'views'] #assets, helpers

  def run(self, edit, index):

    if index >= 0:
   
      self.open_file(index)

    else:

      try:

        self.build_files()
        sublime.active_window().show_quick_panel(self.files, self.open_file)

      except:

        return False

  def is_visible(self, index):

    #return True

    try:

      return self.files[index] and self.show_context_menu

    except: # This should catch all exceptions and return false

      return False
  
  def open_file(self, index):

    if index >= 0:

      sublime.active_window().open_file(os.path.join(self.rails_root_directory, self.files[index]))

  def build_files(self):

    self.files = []
    self.rails_root_directory = rails_root(self.get_working_dir())

    if self.rails_root_directory:

      self.show_context_menu = sublime.load_settings("Rails.sublime-settings").get('show_context_menu')

      current_file_name      = self._active_file_name()
      working_directory      = self.get_working_dir()
      working_directory_base = os.path.basename(working_directory)

      file_name_base         = os.path.basename(current_file_name)
      file_name_base_no_ext  = os.path.splitext(file_name_base)[0]

      rails_app_directory    = os.path.join(self.rails_root_directory, 'app')

      app_sub_directory      = RailsRelatedFilesHelper.get_app_sub_directory(working_directory)

      if app_sub_directory in self.APP_FOLDERS:

        func, args = {
          'controllers': (RailsRelatedFilesHelper.for_controllers, (rails_app_directory, working_directory, file_name_base_no_ext,)),
          'views'      : (RailsRelatedFilesHelper.for_views,       (rails_app_directory, working_directory,)),
          'models'     : (RailsRelatedFilesHelper.for_models,      (rails_app_directory, working_directory, file_name_base_no_ext,))
        }.get(app_sub_directory)

        self.files = func(*args)

        if not self.files:
          self.files = ['Rails Related Files: Nothing found...']


  def description(self, index):
    self.build_files()
    try:
      return self.files[index]
    except IndexError, e:
      return

  # Taken from Git Plugin (Changed .active_view() to .view)
  def _active_file_name(self):
    view = self.view;
    if view and view.file_name() and len(view.file_name()) > 0:
      return view.file_name()

  # Taken from Git Plugin
  def get_working_dir(self):
    file_name = self._active_file_name()
    if file_name:
      return os.path.dirname(file_name)
    else:
      return self.window.folders()[0]

