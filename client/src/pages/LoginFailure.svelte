<script>
  import { linkHandle } from 'svelte-micro'
  import { fly } from 'svelte/transition'
  import { elasticOut } from 'svelte/easing'
</script>

<main class="tinted flex items-center justify-center min-h-screen p-6">
  <div
    in:fly|global={{ x: 160, duration: 250, easing: elasticOut }}
    class="cartoon-box min-w-min w-4/5 max-w-md shadow px-6 py-6 text-left"
  >
    <h3 class="text-3xl font-medium mb-4">⚠️ Login failure</h3>
    <p class="pb-4">Please check your email and password and try again.</p>

    <a
      class="cartoon-box block w-max hover focus cursor-pointer px-6 py-2 font-medium focus:outline-none"
      href="/login"
      use:linkHandle
    >
      Try again
    </a>
  </div>
</main>
