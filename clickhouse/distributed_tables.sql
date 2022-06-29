CREATE TABLE tutorial.hits_v1_all ON CLUSTER '{cluster}' AS tutorial.hits_v1_local
ENGINE Distributed('{cluster}', 'tutorial', 'hits_v1_local', rand());

CREATE TABLE tutorial.visits_v1_all ON CLUSTER '{cluster}' AS tutorial.visits_v1_local
ENGINE = Distributed('{cluster}', 'tutorial', 'visits_v1_local', rand());
