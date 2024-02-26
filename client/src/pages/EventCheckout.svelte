<script>
  import { fly } from 'svelte/transition'
  import { backOut } from 'svelte/easing'
  import { query, linkHandle } from 'svelte-micro'
  import revoluteQrUrl from '../assets/RevoluteQR.png'

  $: id = new URLSearchParams($query)?.get('id')
</script>

{#if id !== null && id !== '' && Number(id) > 0}
  <main class="tinted flex items-center justify-center min-h-screen">
    <div
      in:fly|global={{ x: 160, duration: 250, easing: backOut }}
      class="cartoon-box min-w-min w-4/5 max-w-sm shadow px-6 py-6 text-left"
    >
      <h3 class="text-3xl font-medium mb-6">Checkout</h3>

      <div class="flex justify-center mb-6">
        <img width="250px" src={revoluteQrUrl} alt="Revolute Payment QR Code" />
      </div>

      <p class="text-gray-600 block mb-6">
        Please scan the QR code with your Revolute app and pay the specified in the event details
        amount to complete your registration.
      </p>

      <a
        href={`/event?id=${id}`}
        use:linkHandle
        class="cartoon-box hover focus h-min cursor-pointer px-6 py-2 font-medium focus:outline-none"
      >
        Open Event
      </a>
    </div>
  </main>
{/if}
