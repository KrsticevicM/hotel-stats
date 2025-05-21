# 📘 Semantic Inferences – TP2

This document describes the semantic inference rules applied to the RDF data using the ontology created in this project.

---

## 📄 Inferred Classes

| Inferred Class          | Rule File (`.rq`)                | Applied Condition (Rule)                              | SPARQL Query Example           |
|-------------------------|----------------------------------|--------------------------------------------------------|--------------------------------|
| `:LongStay`             | `infer_LongStay.rq`              | weekNights + weekendNights > 7                         | `?b a :LongStay`               |
| `:TooLongStay`          | `infer_TooLongStay.rq`           | weekNights + weekendNights > 50                        | `?b a :TooLongStay`            |
| `:ShortNoticeBooking`   | `infer_ShortNoticeBooking.rq`    | leadTime < 3                                           | `?b a :ShortNoticeBooking`     |
| `:HighADRBooking`       | `infer_HighADRBooking.rq`        | adr > 150                                              | `?b a :HighADRBooking`         |
| `:SingleAdult`          | `infer_SingleAdult.rq`           | numberOfAdults = 1                                     | `?b a :SingleAdult`            |
| `:FamilyWithBabies`     | `infer_FamilywithBabies.rq`      | babies ≥ 1                                             | `?b a :FamilyWithBabies`       |
| `:RepeatCustomer`       | `infer_RepeatCustomer.rq`        | isRepeatedGuest = true or "1"                          | `?b a :RepeatCustomer`         |

---

## ℹ️ Usage Notes for Backend / Frontend

- All classes are inferred through SPARQL rules and are added directly into the RDF graph.
- You can query them like this:
  ```sparql
  PREFIX : <http://example.org/hotel-ontology/1.0.0.3#>
  SELECT ?booking WHERE {
    ?booking a :HighADRBooking .
  }

