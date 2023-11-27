import { ref } from 'vue';

export function useFetch(url) {
  const data = ref(null);
  const error = ref(null);

  fetch(url, {
      headers: {
        'content-type': 'application/json'
      }
    })
    .then(res => {
      if (!res.ok) {
        const error = new Error(res.statusText);
        error.json = res.json();

        throw error;
      }

      return res.json();
    })
    .then(json => {
        data.value = json;
    })
    .catch(err => {
      error.value = err;

      if (err.json) {
        return err.json.then(json => {
          error.value.message = json;
        });
      }
    });

  return { data, error };
}