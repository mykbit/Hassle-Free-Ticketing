<script>
  import { query, linkHandle } from 'svelte-micro'
  import { fly } from 'svelte/transition'
  import { backOut } from 'svelte/easing'
  import { getEvent, getUser, registerForEvent } from '../lib/api'

  $: id = new URLSearchParams($query)?.get('id')

  let redistered = false
  const register = () => registerForEvent(Number(id)).then(() => (redistered = true))
</script>

{#if id !== null && id !== '' && Number(id) > 0}
  {#await Promise.all([getUser(), getEvent(Number(id))]) then [user, event]}
    <main class="tinted flex items-center justify-center min-h-screen p-6">
      <div
        in:fly|global={{ x: 160, duration: 250, easing: backOut }}
        class="cartoon-box lg:min-w-min lg:w-3/4 w-screen max-w-3xl shadow px-6 py-6 text-left"
      >
        <h3 class="text-3xl font-medium mb-6">{event.eventDetails.name}</h3>

        <div class="block justify-between lg:flex">
          <div class="mb-4 lg:mb-0">
            <p>
              {event.eventDetails.date}
              <span class="text-gray-600 max-sm:hidden">•</span>
              <br class="hidden max-sm:inline" />
              €{event.eventDetails.price} for a ticket
            </p>

            <p class="text-gray-600 mb4">Eventholder: {event.eventDetails.holder_email}</p>
          </div>
          <div class="flex items-end">
            {#if user.email === event.eventDetails.holder_email}
              <a
                href={`/event/upload-statement?id=${event.eventDetails.id}`}
                use:linkHandle
                class="cartoon-box hover focus h-min cursor-pointer px-6 py-2 font-medium focus:outline-none"
              >
                Load bank statement
              </a>
            {:else if !(event.isRegistered || redistered) && !event.isPaid}
              <button
                class="cartoon-box hover focus cursor-pointer px-6 py-2 font-medium focus:outline-none"
                on:click={register}
              >
                Register
              </button>
            {:else if (event.isRegistered || redistered) && !event.isPaid}
              <a
                href={`/event/checkout?id=${event.eventDetails.id}`}
                use:linkHandle
                class="cartoon-box hover focus h-min cursor-pointer px-6 py-2 font-medium focus:outline-none"
              >
                Checkout
              </a>
            {:else}
              <div
                class="cartoon-box hover focus cursor-pointer px-6 py-2 font-medium focus:outline-none"
              >
                Payment verified
              </div>
            {/if}
          </div>
        </div>
      </div>
    </main>
  {:catch}
    <main class="tinted flex items-center justify-center min-h-screen p-6">
      <div
        in:fly|global={{ x: 160, duration: 250, easing: backOut }}
        class="cartoon-box min-w-min w-4/5 max-w-md shadow px-6 py-6 text-left"
      >
        <h3 class="text-3xl font-medium mb-4">Event is not found</h3>
        <p class="pb-4">Looks like this event doesn't exist.</p>
        <a
          href="/"
          use:linkHandle
          class="cartoon-box block w-max hover focus cursor-pointer px-6 py-2 font-medium focus:outline-none"
        >
          Back to home page
        </a>
      </div>
    </main>
  {/await}
{:else}
  <main class="tinted flex items-center justify-center min-h-screen p-6">
    <div
      in:fly|global={{ x: 160, duration: 250, easing: backOut }}
      class="cartoon-box min-w-min w-4/5 max-w-md shadow px-6 py-6 text-left"
    >
      <h3 class="text-3xl font-medium mb-4">Event is not found</h3>
      <p class="pb-4">Looks like this event doesn't exist.</p>
      <a
        href="/"
        use:linkHandle
        class="cartoon-box block w-max hover focus cursor-pointer px-6 py-2 font-medium focus:outline-none"
      >
        Back to home page
      </a>
    </div>
  </main>
{/if}

<!-- {#if user.email === event.eventDetails.holder_email}
<p class="text-gray-600">Load the latest bank statement to validate the tickets.</p>
{:else if !event.isRegistered && !event.isPaid}
<p class="text-gray-600">
  Make sure that you have entered your Revolut name correctly. You can register for
  the event below.
</p>
{:else if event.isRegistered && !event.isPaid}
<p class="text-gray-600">
  If you've made a payment, you're good to go! Make sure that you entered your Revolut
  name correctly.
</p>
{:else}
<p class="text-gray-600">All set!</p>
{/if} -->
