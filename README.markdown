# Sublime Text 2 - Rails Related Files

Note: I've never written any Python code before! So feel free to implement best practices and make a pull request.

This plugin allows you to easily navigate your Rails projects by making a few basic assumptions. I wrote this so I didnt have to constantly use the SideBar to lookup files!

Ok, so lets imagine you "right clicked" on the following file/s (Screenshot 2) or by using the "CMD+Shift+O" shortcut (Screenshot 1)  it will search for files:

 `posts_controller.rb` under `app/controllers`

If it was under the "admin" namespace e.g. `app/controllers/admin/posts_controller.rb` then it will look under `views/admin/posts/**` and vice versa.

    views/posts/** - All files under this folder
    models/post**  - Models starting with "post"

 `show.html.erb` under `app/views/posts`

    models/post**             - Models starting with "post"
    views/posts/**            - All files in this folder
    assets/javascript/post**  - Any javascript file starting with "post"
    assets/stylesheets/post** - Any stylesheet file starting with "post"
    controllers/post**        - Any controller file starting with "post"

 `post.rb` model under `app/models`

    models/post**         - Models starting with "post"
    views/posts/**        - All files in this folder
    views/**/posts/**     - All files in this folder (e.g. admin namespace)
    controllers/post**    - Any controller starting with "post"
    controllers/**/post** - Any controller starting with "post" (e.g. admin namespace)

If you want to disable the context menu, just edit the `Rails.sublime-settings` file changing "show_context_menu" to false.

### Future

Maybe we can extract the possible partials being used in the current file e.g. `render "post"` or even `render @posts`, we know where to look > app/views/posts/_post

### Screenshots

Here I've pressed the shortcut key when looking at the "page.rb" file under models.

Quick Panel

![Quick Panel](https://github.com/luqman/SublimeText2RailsRelatedFiles/raw/master/screenshots/quick-panel.png)

Context Menu

![Context Menu](https://github.com/luqman/SublimeText2RailsRelatedFiles/raw/master/screenshots/context-menu.png)

### Contributors

- https://github.com/bratsche bug fix

### Credits

  - Python version of Rails Inflector https://bitbucket.org/ixmatus/inflector
  - Tiny copy/paste from https://github.com/kemayo/sublime-text-2-git
