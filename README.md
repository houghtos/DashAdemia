# DashAdemia

Scrapes publication metrics using Pubmed (entrez) API and uploads to backend RDS database.  Fully customizable for each author's individual query, default queries, and author aliases (e.g. author changed surname after marriage and has publications under different names).

Data in 1 author to many pulications relationship.  Each publication contains attributes returned by API as well as "author priority" (e.g. were they first, second, third, last, other author on the publication).
