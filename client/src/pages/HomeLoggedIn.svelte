<script>
  import { getUser } from '../lib/api.ts'
  import { fly } from 'svelte/transition'
  import { backOut } from 'svelte/easing'
</script>

<main class="tinted flex items-center justify-center min-h-screen p-6">
  {#await getUser() then { name }}
    <div
      in:fly|global={{ x: 128, duration: 250, easing: backOut }}
      class="cartoon-box min-w-min w-4/5 max-w-lg shadow px-6 py-6 text-left"
    >
      <h3 class="block text-3xl font-medium mb-4">
        Welcome {name}!
      </h3>

      <p class="mb-4">Open a link for an event if you would like to register for it.</p>

      <a class="cartoon-box hover focus block w-max px-6 py-2 font-semibold" href="/event/create">
        Create an Event
      </a>
    </div>
  {/await}
</main>
