# django-staticfiles-redesigned

Inspired by **[Sprockets](https://github.com/sstephenson/sprockets)**, this django app is made to redesign the way django works with static assets.

## Milestones

1. "require" directive, compression, integration wihe CachedStorage, 'runserver' django-command.
2. "require_tree" directive.
3. "require_self"
4. Coffeescript, literate-coffeescript, livescript, sass, compass, less... (compilers(transpilers))
5. Sourcemap.
6. Cache result of compilation, 304 response (for DEV/DEBUG).
7. Compile options.