<script>
  import { linkHandle } from 'svelte-micro'
  import { isLoggedIn } from './api'
</script>

<header class="fixed w-screen px-10 py-6 flex items-center justify-between">
  <a href="/" use:linkHandle class="cartoon-box logo px-2 py-1 font-semibold">
    Hassle-Free Ticketing
  </a>

  <div>
    {#if $isLoggedIn}
      <a href="/logout" class="font-semibold px-2 py-1" use:linkHandle>Logout</a>
    {:else}
      <a href="/login" class="font-semibold px-2 py-1" use:linkHandle>Login</a>
      <a href="/register" class="font-semibold px-2 py-1" use:linkHandle>Register</a>
    {/if}
  </div>
</header>

<style>
  .logo {
    box-shadow: 2px 2px 0px 0px rgba(0, 0, 0, 100);
  }
</style>
