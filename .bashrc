# Color codes
RED='\[\033[0;31m\]'
GREEN='\[\033[0;32m\]'
YELLOW='\[\033[0;33m\]'
BLUE='\[\033[0;34m\]'
MAGENTA='\[\033[0;35m\]'
CYAN='\[\033[0;36m\]'
RESET='\[\033[0m\]'

# Custom prompt
export PS1="${BLUE}\u${YELLOW}@${CYAN}\h${MAGENTA}:\w${GREEN} \$ ${RESET}"
