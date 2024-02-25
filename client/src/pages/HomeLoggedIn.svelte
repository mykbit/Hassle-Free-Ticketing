<script>
  import { getUser } from '../lib/api.ts'
  import { fly } from 'svelte/transition'
  import { backOut } from 'svelte/easing'
  import { linkHandle } from 'svelte-micro'
</script>

<main class="tinted flex items-center justify-center min-h-screen p-6">
  {#await getUser() then { name }}
    <div
      in:fly|global={{ x: 160, duration: 250, easing: backOut }}
      class="cartoon-box min-w-min w-4/5 max-w-lg shadow px-6 py-6 text-left"
    >
      <h3 class="block text-3xl font-medium mb-4">
        👋 Welcome {name}!
      </h3>

      <p class="mb-4">Open the link to an event you would like to register for.</p>

      <a
        class="cartoon-box hover focus block w-max px-6 py-2 font-semibold"
        href="/event/create"
        use:linkHandle
      >
        Create an Event
      </a>
    </div>
  {/await}
</main>
