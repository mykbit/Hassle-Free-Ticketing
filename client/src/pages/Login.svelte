<script>
  import { router, linkHandle } from 'svelte-micro'
  import { login } from '../lib/api'
  import { fly } from 'svelte/transition'
  import { backOut } from 'svelte/easing'

  const onSubmit = (e) => {
    const formData = new FormData(e.target)
    login(formData.get('email'), formData.get('password'))
      .then(() => router.push('/'))
      .catch(() => router.push('/login/failure'))
  }
</script>

<main class="tinted flex items-center justify-center min-h-screen">
  <div
    in:fly|global={{ x: 160, duration: 250, easing: backOut }}
    class="cartoon-box min-w-min w-4/5 max-w-sm shadow px-6 py-6 text-left"
  >
    <h3 class="text-3xl font-medium mb-6">🔑 Login</h3>

    <form on:submit|preventDefault={onSubmit}>
      <div class="mb-4">
        <label for="login-form-email">Email</label>
        <input
          id="login-form-email"
          name="email"
          type="email"
          placeholder="root@tickets.com"
          required
          class="cartoon-box focus w-full px-4 py-2 mt-1 focus:outline-none"
        />
      </div>

      <div class="mb-4">
        <label for="login-form-password">Password</label>
        <input
          id="login-form-password"
          name="password"
          type="password"
          placeholder="••••••••"
          required
          class="cartoon-box focus w-full px-4 py-2 mt-1 focus:outline-none"
        />
      </div>

      <div class="flex items-baseline mb-4 gap-2">
        <input
          id="login-form-submit"
          type="submit"
          value="Login"
          required
          class="cartoon-box hover focus cursor-pointer px-6 py-2 font-medium focus:outline-none"
        />
      </div>

      <div>
        <p class="text-sm text-gray-600">
          Don't have an account?
          <a class="underline" use:linkHandle href="/register">Сlick here to register.</a>
        </p>
      </div>
    </form>
  </div>
</main>
