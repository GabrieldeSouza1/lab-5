COMPLEX_QUERY = '''
query repository($owner: String!, $name: String!, $per_page: Int!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(
      states: [MERGED, CLOSED]
      orderBy: { field: CREATED_AT, direction: DESC }
      first: $per_page
      after: $cursor
    ) {
      edges {
        node {
          title
          number
          state
          createdAt
          closedAt
          mergedAt
          bodyText
          reviewDecision
          reviews {
            totalCount
          }
          files {
            totalCount
          }
          additions
          deletions
          participants {
            totalCount
          }
          comments {
            totalCount
          }
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
'''

SIMPLE_QUERY = '''
query ($per_page: Int!, $cursor: String) {
  search(query: "stars:>0 sort:stars-desc", type: REPOSITORY, first: $per_page, after: $cursor) {
    edges {
      node {
        ... on Repository {
          nameWithOwner
          stargazerCount
          pullRequests {
            totalCount
          }
        }
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
'''