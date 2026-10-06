# MinIO APAC demos

Browser-only demo pages for customer sessions, served with GitHub Pages at
https://minio-apac.github.io/demos/.

| Demo | Path | Notes |
|---|---|---|
| Erasure Coding failure simulator | `ec-simulator/` | Korean UI. Tap drives/nodes to fail them; shows GET/PUT per erasure set. |
| MemKV recompute vs recall | `memkv-recall/` | EN/KO toggle. Replay of a captured single-Mac lab run, not a product benchmark. |

## Layout

- `src/*.html` — page sources, written as Claude Artifact pages (no doctype/head). The same file can be published as an Artifact.
- `build.py` — wraps each source in a full HTML document (charset, viewport, `noindex`) and writes `index.html` / `<name>/index.html`.
- Built files are committed; Pages serves the `main` branch root.

## Update a demo

```bash
./build.py
git add -A && git commit -m "Update <demo>" && git push
```

## Rules for anything published here

This repository and its pages are **public**.

- No internal numbers, source paths, function names, or internal document references.
- No pricing. No unreleased products or features.
- No customer names.
- Performance numbers must state where they come from (official material, or our own lab run with its setup).
- Pages must not call a live cluster or embed credentials.
