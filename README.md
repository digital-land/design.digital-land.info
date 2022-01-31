# GOVUK Flask Prototype Kit

## Getting started

  Optional but recommended. Run in a virtualenv. To create one (with Python 3) run:

  ```
  mkvirtualenv --python=`which python3` <name>
  ```
  where <name> is what you wish to call it.

  When returning run `workon <name>` to activate the virtualenv you just created.

  To install flask and all the other dependencies run:

  ```
  make init
  ```

  To run the Prototype Kit

  ```
  make run
  ```
  
## Usage notes
  
  ### Creating pages
  
  Templates which are used to generate the pages are stored in [`/application/templates`](/application/templates).
  
  A generic route within [`/blueprints/base/views.py`](https://github.com/digital-land/govuk-flask-prototype-kit/blob/efea152dd9bb5c232c7ba7413cbf3a2ca1827466/application/blueprints/base/views.py#L21) attempts to render the path to a given template if the file exists.
  
  **For example:**
  
  `http://domain.tld/pages/ripa-gudiance/prototype-1.html` will try to render a template it expects to be in the file: `application/templates/pages/ripa-guidance/prototype-1.html`
  
  The aim of this is to save time and energy writing and maintaining routes for static template files. If you need something more specific or bespoke then you can still write your own routes which should override the generic route.
  
  ---
  
  ### CSS namespacing
  
  Each page will be automattically generated a html class name. This allows for bepoke CSS for a page or set of pages within this prototype-kit without impacting older or different prototypes.
  
  #### For example:
  
  A page at this URL `http://domain.tld/pages/ripa-gudiance/prototype-1.html` will be generated a classname on the HTML element of:
  `app-ripa-guidance-prototype-1` which follows the format: `app-[folder-name]-[filename]`
  
  Which can be used to write CSS to target: 
  
  **A set of pages:**
  
  ```scss
  [class*='app-ripa-guidance'] {
    .selector-here { 
      display: block; 
    }
  }
  ```
  
  This would impact: `http://domain.tld/pages/ripa-gudiance/prototype-1.html` and `http://domain.tld/pages/ripa-gudiance/prototype-2.html` as they both live within `ripa-guidance`
  
  **An individual page:**
  
  ```scss
  .app-ripa-guidance-prototype-1 {
    .selector-here { 
      display: block; 
    }
  }
  ```
  
  See an example in [`assets/scss/versions/_ripa.scss`](/assets/scss/versions/_ripa.scss)
