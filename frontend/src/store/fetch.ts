let API_URL = '';

if (process.env.NODE_ENV !== 'development') {
  API_URL = 'https://api-dot-game-remix-guesser.uw.r.appspot.com/';
}

// eslint-disable-next-line
export function fetchApi(url: string, config?: object) {
  return fetch(`${API_URL}${url}`, config);
}
