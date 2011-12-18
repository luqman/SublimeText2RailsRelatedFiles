# Sublime Text 2 - Rails Related Files

Note: I've never written any Python code before! So feel free to implement best practices and make a pull request.

I've made a few assumptions; e.g. take a Blog app with the "Post" model/view/controller.

So when "Right Clicking" on the active view or using the "CMD+Shift+O" shortcut it will look for files.

  "posts_controller.rb" under app/controllers

    views/posts/** - folder for view files
    models/post** - any models starting with "post"

  "show.html.erb" under app/views/posts

    models/post** - any models starting with "post"
    views/posts/** - all files this folder
    assets/javascript/post** - anyjavascript file starting with "post"
    assets/stylesheets/post** - any stylesheet file starting with "post"
    controllers/post** - any controller file starting with "post"

  "post.rb" model under app/models

    models/post** - any models starting with "post"
    views/posts/** - folder for view files
    views/**/posts/**
    controllers/post** - any controller file starting with "post"

If you want to disable the context menu, just edit the "Rails.sublime-settings" file changing "show_context_menu" to false.

### Future

Maybe we can extract the possible partials being used in the current file e.g. `render "post"` or even `render @posts`, we know where to look > app/views/posts/_post

### Screenshots

![Quick Panel](https://github.com/luqman/SublimeText2RailsRelatedFiles/raw/master/screenshots/quick-panel.png)
![Context Menu](https://github.com/luqman/SublimeText2RailsRelatedFiles/raw/master/screenshots/context-menu.png)

### Credits

  - https://bitbucket.org/ixmatus/inflector
  - Tiny copy/paste from https://github.com/kemayo/sublime-text-2-git