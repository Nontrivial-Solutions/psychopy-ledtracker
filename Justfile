set export

@_default:
    just --list

# Set up development environment
bootstrap:
    if test ! -e .venv; then \
      git submodule deinit -f . ;\
      git submodule update --init --recursive ; \
      prek install -f -c .pre-commit-config.yaml ; \
      uv venv --python 3.13 && uv sync ;\
    fi

refresh-sub: 
      git submodule deinit -f . 
      git submodule update --init --recursive 

##################################################################################################
## mkdocs     ####################################################################################
##################################################################################################

# Build docs 
html: bootstrap
    source .venv/bin/activate && \
    mkdocs build -d ./.build/docs

# Luanch live docs 
live: bootstrap
    @echo "🚀 Check port 8000"
    source .venv/bin/activate && \
    mkdocs serve --livereload --dev-addr 0.0.0.0:8000

##################################################################################################
## formatting  ###################################################################################
##################################################################################################

##################################################################################################
####### tombi format ##########################################################################
##################################################################################################
    
# Run tombi 
do-tombi:
    tombi format psychopy_ledstrip 
    tombi format docs 
    tombi format ./pyproject.toml 
    tombi format ./.rumdl.toml 
    

##################################################################################################
####### rumdl format ##########################################################################
##################################################################################################
    
# Run rumdl 
do-rumdl:
    rumdl fmt docs

##################################################################################################
####### check everything #########################################################################
##################################################################################################
check-todo:
    if test -e .todo; then \
      echo "👎 Found a todo" ;\
      exit 1 ;\
    fi
    echo "👍 Found no todo"
    exit 0


##################################################################################################
####### ruff format ##########################################################################
##################################################################################################

# Run ruff 
do-ruff:
    ruff check --fix psychopy_ledstrip 
    ruff format psychopy_ledstrip 

# Generate warnings from ruff
warning-ruff:
    -ruff check psychopy_ledstrip --output-format json -o .build/ruff/ruff.json | ciqar -r ruff:.build/ruff/ruff.json -s psychopy_ledstrip -o .build/ruff

# Cyclically Generate warnings from ruff 
c-warning-ruff:
    -watch -n 3 just warning-ruff


# Server ruff results
[working-directory: '.build/ruff']
serve-ruff: warning-ruff
    @echo "🚀 Check port 1315"
    python -m reloadserver 1315

##################################################################################################
####### check everything #########################################################################
##################################################################################################

# Check all style and formatting. Fail on warning.  
check: 
    prek run --all-files
    @echo "🚀 Checked the files"
    exit 0

# Check all style and formatting. Fail on warning.  
check-release: check check-todo
    exit 0

##################################################################################################
####### Test #####################################################################################
##################################################################################################

# Check all style and formatting. Fail on warning.  
test: 
    pytest 

##################################################################################################
####### all format ###############################################################################
##################################################################################################

# Run all formatting.  
format: do-ruff do-rumdl do-tombi
    @echo "🚀 Formated the files"
    exit 0