<script lang="ts">
  import { Route, path, router } from 'svelte-micro'
  import { isLoggedIn } from './lib/api.js'
  import HomeLoggedIn from './pages/HomeLoggedIn.svelte'
  import Header from './lib/Header.svelte'
  import Event from './pages/Event.svelte'
  import CreateEvent from './pages/CreateEvent.svelte'
  import Login from './pages/Login.svelte'
  import LoginFailure from './pages/LoginFailure.svelte'
  import Register from './pages/Register.svelte'
  import RegisterFailure from './pages/RegisterFailure.svelte'
  import './styles/main.css'
  import EventUploadStatement from './pages/EventUploadStatement.svelte'

  if ('scrollRestoration' in history) history.scrollRestoration = 'manual'
  path.subscribe(() => window.scrollTo({ top: 0 }))

  const logout = () => {
    $isLoggedIn = false
    localStorage.removeItem('token')
    router.push('/')
  }
</script>

<Route>
  <Header />
  {#if $isLoggedIn}
    <Route path="/"><HomeLoggedIn /></Route>

    <Route path="/event">
      <Route path="/"><Event /></Route>
      <Route path="/create"><CreateEvent /></Route>
      <Route path="/checkout">...</Route>
      <Route path="/upload-statement"><EventUploadStatement /></Route>
    </Route>

    <Route path="/logout">{logout()}</Route>

    <Route fallback>{router.replace('/')}</Route>
  {:else}
    <Route path="/">{router.replace('/login')}</Route>

    <Route path="/login">
      <Route path="/"><Login /></Route>
      <Route path="/failure"><LoginFailure /></Route>
    </Route>

    <Route path="/register">
      <Route path="/"><Register /></Route>
      <Route path="/failure"><RegisterFailure /></Route>
    </Route>

    <Route fallback>{router.replace('/login')}</Route>
  {/if}
</Route>
