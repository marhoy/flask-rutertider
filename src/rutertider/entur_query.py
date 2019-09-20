import random

import requests

# For testing of queries, use this page:
# https://api.entur.org/doc/shamash-journeyplanner/


def create_departure_query(stop_id, max_departures=10):
    """Create a GraphQL query, finding all departures for a specific stop_id

    Args:
        stop_id: The stop_id you want departures for
        max_departures: The maximum number of departures to return

    Returns:
        A GraphQL query
    """
    departure_query = """
    {
      stopPlace(id: "STOP_PLACE" ) {
        name
        estimatedCalls(numberOfDepartures: MAX_DEPARTURES ) {
          quay {
            id
            description
          }
          expectedDepartureTime
          actualDepartureTime
          realtime
          realtimeState
          destinationDisplay {
            frontText
          }
          serviceJourney {
            line {
              id
              publicCode
              presentation {
                colour
                textColour
              }
            }
          }
        }
      }
    }
    """.replace('STOP_PLACE', stop_id).\
        replace('MAX_DEPARTURES', str(max_departures))
    return departure_query


def create_departure_query_whitelist(stop_id, line_ids, max_departures=5):
    departure_query = """
    {
      stopPlace(id: "STOP_PLACE") {
        name
            estimatedCalls(
          numberOfDepartures: MAX_DEPARTURES
          whiteListed: {
                lines: LIST_OF_LINE_IDS
            }
        ) {
          expectedArrivalTime
          expectedDepartureTime
          quay {
            id
            description
          }
          destinationDisplay {
            frontText
          }
                serviceJourney {
            line {
              id
              publicCode
              presentation {
                colour
                textColour
              }
                    }
          }
        }
      }
    }
    """.replace('STOP_PLACE', stop_id). \
        replace('MAX_DEPARTURES', str(max_departures)). \
        replace('LIST_OF_LINE_IDS', str(line_ids).replace("'", '"'))
    return departure_query


def create_situation_query(line_ids):
    """Create a GraphQL query, finding all situations for a specific line_id

    Args:
        line_ids: A list of line_ids you want situations for

    Returns:
        A GraphQL query
    """
    situation_query = """
    {
      lines(ids: LIST_OF_LINE_IDS) {
        id
        publicCode
        transportMode
        presentation {
          textColour
          colour
        }
        situations {
          summary {
            value
            language
          }
          description {
            value
            language
          }
          advice {
            value
            language
          }
          validityPeriod {
            startTime
            endTime
          }
        }
      }
    }
    """.replace('LIST_OF_LINE_IDS', str(line_ids).replace("'", '"'))
    return situation_query


def journey_planner_api(query):
    """Query the Entur Journey Planner API

    Args:
        query: A string with the GraphQL query

    Returns:
        A requests response object
    """
    query_url = 'https://api.entur.io/journey-planner/v2/graphql'
    headers = {'ET-Client-Name': 'flask - avgangstider_{:03}'.format(
        random.randint(0, 999))}
    response = requests.post(query_url, headers=headers, json={'query': query})
    response.raise_for_status()
    return response