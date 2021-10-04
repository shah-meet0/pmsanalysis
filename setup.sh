mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
[theme]
base = 'light'
primaryColor='#6eb52f'
backgroundColor='#f0f0f5'
secondaryBackgroundColor='#e0e0ef'
textColor='#262730'
font='sans serif'
" > ~/.streamlit/config.toml
