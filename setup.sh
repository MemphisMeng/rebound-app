mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"qemail@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
PORT = $PORT\n\
" > ~/.streamlit/config.toml
