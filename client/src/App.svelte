<script lang="ts">
  import { Route, path, router } from 'svelte-micro'
  import { isLoggedIn } from './lib/api.js'
  import Login from './pages/Login.svelte'
  import LoginFailure from './pages/LoginFailure.svelte'
  import Register from './pages/Register.svelte'
  import RegisterFailure from './pages/RegisterFailure.svelte'
  import './styles/main.css'
  import HomeLoggedIn from './pages/HomeLoggedIn.svelte'
  import Header from './lib/Header.svelte'

  if ('scrollRestoration' in history) history.scrollRestoration = 'manual'
  path.subscribe(() => window.scrollTo({ top: 0 }))
</script>

<Route>
  {#if $isLoggedIn}
    <Header></Header>
    <Route path="/"><HomeLoggedIn /></Route>

    <Route fallback>{router.replace('/')}</Route>
  {:else}
    <Route path="/">{router.replace('/register')}</Route>

    <Route path="/login">
      <Route path="/"><Login /></Route>
      <Route path="/failure"><LoginFailure /></Route>
    </Route>

    <Route path="/register">
      <Route path="/"><Register /></Route>
      <Route path="/failure"><RegisterFailure /></Route>
    </Route>

    <Route fallback>{router.replace('/register')}</Route>
  {/if}
</Route>
