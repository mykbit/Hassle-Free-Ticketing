<script>
  import { query, linkHandle } from 'svelte-micro'
  import { apiBaseUrl, getToken } from '../lib/api'
  import { fly } from 'svelte/transition'
  import { backOut } from 'svelte/easing'

  function handleSubmit(event) {
    const form = event.currentTarget
    const url = new URL(form.action)
    const formData = new FormData(form)
    const searchParams = new URLSearchParams(formData)

    const fetchOptions = {
      method: form.method,
      headers: {
        Authorization: 'Bearer ' + getToken(),
      },
    }

    if (form.method.toLowerCase() === 'post') {
      if (form.enctype === 'multipart/form-data') {
        fetchOptions.body = formData
      } else {
        fetchOptions.body = searchParams
      }
    } else {
      url.search = searchParams
    }

    fetch(url, fetchOptions).then((response) => {
      if (response.ok) {
        success = true
      } else {
        success = false
      }
    })

    event.preventDefault()
  }

  let success = null

  $: id = new URLSearchParams($query)?.get('id')
</script>

<main class="tinted flex items-center justify-center min-h-screen p-6">
  {#if id !== null && id !== '' && Number(id) > 0}
    {#if success == null}
      <div
        in:fly|global={{ x: 160, duration: 250, easing: backOut }}
        class="cartoon-box lg:min-w-min lg:w-3/4 w-screen max-w-3xl shadow px-6 py-6 text-left"
      >
        <h3 class="text-3xl font-medium mb-6">📄 Upload bank statement</h3>

        <form
          on:submit={handleSubmit}
          action={`${apiBaseUrl}/bank-statement/${id}`}
          method="POST"
          enctype="multipart/form-data"
          required
          accept=".csv"
        >
          <input
            class="block w-full text-sm px-4 py-2 mt-1 cartoon-box focus mb-4 file:mr-4 file:py-2 file:px-4 file:rounded-md
        file:border-0 file:text-sm file:font-semibold
        file:bg-transparent cursor-pointer hover"
            id="upload-statement-form"
            name="file"
            type="file"
          />

          <button
            class="cartoon-box hover focus cursor-pointer px-6 py-2 font-medium focus:outline-none"
          >
            Upload
          </button>
        </form>
      </div>
    {:else if success === true}
      <div
        in:fly|global={{ x: 160, duration: 250, easing: backOut }}
        class="cartoon-box lg:min-w-min lg:w-3/4 w-screen max-w-3xl shadow px-6 py-6 text-left"
      >
        <h3 class="text-3xl font-medium mb-4">🎯 Upload success</h3>

        <a
          class="cartoon-box block w-max hover focus cursor-pointer px-6 py-2 font-medium focus:outline-none"
          href="/event?id={id}"
          use:linkHandle
        >
          Go back
        </a>
      </div>
    {:else if success === false}
      <div
        in:fly|global={{ x: 160, duration: 250, easing: backOut }}
        class="cartoon-box lg:min-w-min lg:w-3/4 w-screen max-w-3xl shadow px-6 py-6 text-left"
      >
        <h3 class="text-3xl font-medium mb-4">⚠️ Upload failure</h3>
        <p class="pb-4">An error occured during file uploading.</p>

        <button
          class="cartoon-box block w-max hover focus cursor-pointer px-6 py-2 font-medium focus:outline-none"
          on:click={() => (success = null)}
        >
          Try again
        </button>
      </div>
    {/if}
  {/if}
</main>
