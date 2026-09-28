const App = () => {
  return (
    <main className="min-h-screen bg-stone-950 text-white flex items-center justify-center px-6">
      <div className="w-full max-w-4xl text-center">
        {/* Logo */}
        <p className="mb-10 text-sm font-semibold tracking-[0.35em] text-stone-400 uppercase">
          OLFARA
        </p>

        {/* Main content */}
        <h1 className="text-5xl font-semibold tracking-tight sm:text-7xl">
          Discover your
          <span className="block text-stone-400">next signature scent.</span>
        </h1>

        <p className="mx-auto mt-6 max-w-lg text-base leading-7 text-stone-400 sm:text-lg">
          A fragrance discovery marketplace connecting you with vendors that
          have the scents you’re looking for.
        </p>

        {/* Coming soon */}
        <div className="mt-10 inline-flex items-center gap-2 rounded-full border border-stone-800 bg-stone-900 px-5 py-2.5 text-sm text-stone-300">
          <span className="h-2 w-2 rounded-full bg-emerald-400" />
          Coming soon
        </div>

        {/* Footer */}
        <p className="mt-16 text-xs text-stone-600">
          © {new Date().getFullYear()} OLFARA
        </p>
      </div>
    </main>
  );
};

export default App;
