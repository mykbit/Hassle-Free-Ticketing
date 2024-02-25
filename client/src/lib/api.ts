import { writable, type Writable } from 'svelte/store'

export const apiBaseUrl = import.meta.env.CLIENT_API_URL as string

type ResponseDataWrapper<Data> = {
  error: string | null
  data: Data
  message: string
}

// --- Token ---

export type TokenEntry = {
  token: string
  expiryDate: number
}

export const getToken = (storageKey = 'token'): TokenEntry['token'] | null => {
  const entry: string | null = localStorage.getItem(storageKey)
  if (entry === null) return null

  const tokenEntry: TokenEntry = JSON.parse(entry) as TokenEntry
  if (tokenEntry.expiryDate > Date.now()) {
    localStorage.removeItem(storageKey)
    return null
  }

  return tokenEntry.token
}

export const setToken = (tokenEntry: TokenEntry, storageKey = 'token'): TokenEntry['token'] => {
  localStorage.setItem(storageKey, JSON.stringify(tokenEntry))
  return tokenEntry.token
}

export const register = async (
  email: string,
  password: string,
  name: string
): Promise<TokenEntry['token']> => {
  const response: Response = await fetch(`${apiBaseUrl}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, name }),
  })

  if (!response.ok) throw new Error('Failed to register')

  const result: ResponseDataWrapper<TokenEntry> = await response.json()

  isLoggedIn.set(true)
  return setToken(result.data)
}

export const login = async (email: string, password: string): Promise<TokenEntry['token']> => {
  const response: Response = await fetch(`${apiBaseUrl}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })

  if (!response.ok) throw new Error('Failed to login')

  const result: ResponseDataWrapper<TokenEntry> = await response.json()

  isLoggedIn.set(true)
  return setToken(result.data)
}

export const isLoggedIn: Writable<boolean> = writable(getToken() !== null)

export const getUser = async (): Promise<{ email: string; name: string }> => {
  const token = getToken()
  if (token === null) throw new Error('Not logged in')

  const response: Response = await fetch(`${apiBaseUrl}/user`, {
    headers: { Authorization: `Bearer ${token}` },
  })

  if (!response.ok) throw new Error('Failed to get user')

  const result: ResponseDataWrapper<{ email: string; name: string }> = await response.json()
  return result.data
}

export const createEvent = async (name: string, ticketPrice: number, date: string) => {
  const token = getToken()
  if (token === null) throw new Error('Not logged in')

  const response: Response = await fetch(`${apiBaseUrl}/user`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ name, ticketPrice, date }),
  })

  if (!response.ok) throw new Error('Failed to create event')

  const result: ResponseDataWrapper<number> = await response.json()
  return result
}
