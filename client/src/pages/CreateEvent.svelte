<script>
  import { linkHandle, router } from 'svelte-micro'
  import { register } from '../lib/api'
  import { fly } from 'svelte/transition'
  import { backOut } from 'svelte/easing'

  const onSubmit = (e) => {
    const formData = new FormData(e.target)
    register(formData.get('name'), formData.get('price'), formData.get('date'))
      .then(() => router.push('/'))
      .catch(() => router.push('/register/failure'))
  }
</script>

<main class="tinted flex items-center justify-center min-h-screen p-6">
  <div
    in:fly|global={{ x: 128, duration: 250, easing: backOut }}
    class="cartoon-box min-w-min w-4/5 max-w-md shadow px-6 py-6 text-left"
  >
    <h3 class="text-3xl font-medium mb-6">Registration</h3>

    <form on:submit|preventDefault={onSubmit}>
      <div class="mb-4">
        <label for="event-form-name">Event Name</label>
        <input
          id="event-form-name"
          name="name"
          type="text"
          placeholder="Computer Science Socializing Event"
          required
          class="cartoon-box focus w-full px-4 py-2 mt-1 mb-1 focus:outline-none"
        />
        <p class="text-sm text-gray-600">Make sure that you have entered your Revolut name.</p>
      </div>

      <div class="mb-4">
        <label for="event-form-price">Price (in €)</label>
        <input
          id="event-form-price"
          name="price"
          type="number"
          placeholder="7"
          required
          class="cartoon-box focus w-full px-4 py-2 mt-1 focus:outline-none"
        />
      </div>

      <div class="mb-4">
        <label for="event-form-password">Password</label>
        <input
          id="event-form-date"
          name="date"
          type="date"
          placeholder=""
          required
          class="cartoon-box focus w-full px-4 py-2 mt-1 focus:outline-none"
        />
      </div>

      <div class="flex mb-4 items-baseline gap-2">
        <input
          id="event-form-submit"
          type="submit"
          value="Create Event"
          class="cartoon-box hover focus cursor-pointer px-6 py-2 font-medium focus:outline-none"
        />
      </div>

      <div>
        <p class="text-sm text-gray-600">
          Already have an account?
          <a class="underline" use:linkHandle href="/login">Сlick here to login.</a>
        </p>
      </div>
    </form>
  </div>
</main>
