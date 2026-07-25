import { useAuth } from "./AuthProvider";

export default function LoginPage() {
  const { login } = useAuth();
  // TODO (you): enter the app in demo mode.
  function onSkip() {}

  return (
    <div className="min-h-screen bg-white">
      <div className="mx-auto flex min-h-screen max-w-sm flex-col px-6">
        {/* Hero — centered in the available space */}
        <main className="flex flex-1 flex-col items-center justify-center text-center">
          <div className="grid h-16 w-16 place-items-center rounded-2xl bg-indigo-600 shadow-lg shadow-indigo-500/30">
            <svg
              className="h-8 w-8"
              viewBox="0 0 24 24"
              fill="none"
              stroke="white"
              strokeWidth="2.2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <polyline points="4 15 9 10 13 14 20 6" />
            </svg>
          </div>

          <h1 className="mt-6 text-4xl font-bold tracking-tight text-slate-900">
            Quiet
          </h1>
          <p className="mt-3 text-base leading-relaxed text-slate-500">
            Calm money, clearly tracked. Household and personal, side by side.
          </p>
        </main>

        {/* Bottom actions */}
        <footer className="pb-10">
          <button
            type="button"
            onClick={login}
            className="flex w-full items-center justify-center gap-3 rounded-2xl border border-slate-200 bg-white py-4 font-semibold text-slate-900 shadow-sm transition hover:bg-slate-50 active:scale-[0.99]"
          >
            <svg className="h-5 w-5" viewBox="0 0 48 48" aria-hidden="true">
              <path
                fill="#EA4335"
                d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"
              />
              <path
                fill="#4285F4"
                d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"
              />
              <path
                fill="#FBBC05"
                d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"
              />
              <path
                fill="#34A853"
                d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"
              />
            </svg>
            Continue with Google
          </button>

          <button
            type="button"
            onClick={onSkip}
            className="mt-5 w-full text-sm font-semibold text-slate-900 hover:text-slate-600"
          >
            Skip — explore the demo
          </button>

          <p className="mt-5 text-center text-xs leading-relaxed text-slate-400">
            By continuing you agree to the Terms and Privacy Policy.
          </p>
        </footer>
      </div>
    </div>
  );
}
