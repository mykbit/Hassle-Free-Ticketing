<script>
  import { linkHandle, router } from 'svelte-micro'
  import { register } from '../lib/api'
  import { fly } from 'svelte/transition'
  import { backOut } from 'svelte/easing'

  const onSubmit = (e) => {
    const formData = new FormData(e.target)
    register(formData.get('email'), formData.get('password'), formData.get('name'))
      .then(() => router.push('/'))
      .catch(() => router.push('/register/failure'))
  }
</script>

<main class="tinted flex items-center justify-center min-h-screen p-6">
  <div
    in:fly|global={{ x: 160, duration: 250, easing: backOut }}
    class="cartoon-box min-w-min w-4/5 max-w-md shadow px-6 py-6 text-left"
  >
    <h3 class="text-3xl font-medium mb-6">📝 Registration</h3>

    <form on:submit|preventDefault={onSubmit}>
      <div class="mb-4">
        <label for="register-form-name">Full Name</label>
        <input
          id="register-form-name"
          name="name"
          type="text"
          placeholder="John Smith"
          required
          class="cartoon-box focus w-full px-4 py-2 mt-1 mb-1 focus:outline-none"
        />
        <p class="text-sm text-gray-600">Make sure that you have entered your Revolut name.</p>
      </div>

      <div class="mb-4">
        <label for="register-form-email">Email</label>
        <input
          id="register-form-email"
          name="email"
          type="email"
          placeholder="root@tickets.com"
          required
          class="cartoon-box focus w-full px-4 py-2 mt-1 focus:outline-none"
        />
      </div>

      <div class="mb-4">
        <label for="register-form-password">Password</label>
        <input
          id="register-form-password"
          name="password"
          type="password"
          placeholder="••••••••"
          required
          class="cartoon-box focus w-full px-4 py-2 mt-1 focus:outline-none"
        />
      </div>

      <div class="flex mb-4 items-baseline gap-2">
        <input
          id="register-form-submit"
          type="submit"
          value="Register"
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
