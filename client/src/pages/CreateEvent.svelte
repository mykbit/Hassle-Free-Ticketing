<script>
  import { linkHandle, router } from 'svelte-micro'
  import { createEvent } from '../lib/api'
  import { fly } from 'svelte/transition'
  import { backOut } from 'svelte/easing'

  const onSubmit = (e) => {
    const formData = new FormData(e.target)
    createEvent(formData.get('name'), formData.get('price'), formData.get('date'))
      .then((id) => router.push(`/event?id=${id}`))
      .catch(() => router.push('/event/create/failure'))
  }
</script>

<main class="tinted flex items-center justify-center min-h-screen p-6">
  <div
    in:fly|global={{ x: 160, duration: 250, easing: backOut }}
    class="cartoon-box min-w-min w-4/5 max-w-md shadow px-6 py-6 text-left"
  >
    <h3 class="text-3xl font-medium mb-6">🎉 Create Event</h3>

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
      </div>

      <div class="mb-4">
        <label for="event-form-price">Price for a ticket (in €)</label>
        <input
          id="event-form-price"
          name="price"
          type="number"
          placeholder="7"
          min="0"
          max="1000"
          required
          class="cartoon-box focus w-full px-4 py-2 mt-1 focus:outline-none"
        />
      </div>

      <div class="mb-6">
        <label for="event-form-date">Date</label>
        <input
          id="event-form-date"
          name="date"
          type="date"
          required
          class="cartoon-box focus w-full px-4 py-2 mt-1 focus:outline-none"
        />
      </div>

      <div class="flex mb-0 items-baseline gap-2">
        <input
          id="event-form-submit"
          type="submit"
          value="Create Event"
          class="cartoon-box hover focus cursor-pointer px-6 py-2 font-medium focus:outline-none"
        />
      </div>
    </form>
  </div>
</main>
